import { useState, useEffect, useCallback, useRef } from 'react';
import { debounce, throttle } from 'lodash';
import PropTypes from 'prop-types'
import { useConversationSocket, useListConfigurationOptions, useGetConversation } from '/src/modules/common/clients/useCleonApi';


export const ChatEventType = {
    STATUS: "status",
    MESSAGE: "message"
}

export const ChatMessageType = {
    HUMAN_MESSAGE: "human_message",
    AI_MESSAGE: "ai_message",
    SETTINGS: "update_settings",
}

/**
 * useChat (Controller Layer) is a custom hook for managing the chat state. It keeps the main logic for interacting with the chat.
 */
function useChat(chatId) {
    const { data: conversation, refetch: getConversation } = useGetConversation(chatId)
    const { data: settingOptions } = useListConfigurationOptions()
    const [messageHistory, setMessageHistory] = useState([]);
    const [chatHistory, setChatHistory] = useState([]);
    const { sendMessage, lastMessage, readyState } = useConversationSocket(chatId);
    const [isDirty, setIsDirty] = useState(false);
    const [currentSettings, setCurrentSettings] = useState({ model: null, temperature: null });
    const messageQueue = useRef([])

    useEffect(() => {
        setCurrentSettings({
            model: conversation?.model,
            temperature: conversation?.configuration?.temperature
        })
    }, [conversation]);

    /**
     * useEffect for handling incoming messages of type STATUS from the chat socket.
     */
    useEffect(() => {
        const event = lastMessage?.data ? JSON.parse(lastMessage.data) : null
        if (!(event?.type === ChatEventType.STATUS)) {
            return
        }
        const messageType = event.data.message_type
        switch (messageType) {
            case ChatMessageType.SETTINGS:
                getConversation()
                break
            case ChatMessageType.HUMAN_MESSAGE:
                if (messageHistory.length > 0) {
                    processMessageHistory.current(messageHistory.join(""))
                }
                break
        }
    }, [lastMessage, messageHistory]);

    /**
     * useEffect for handling incoming messages of type MESSAGE from the chat socket.
     */
    useEffect(() => {
        const event = lastMessage?.data ? JSON.parse(lastMessage.data) : null
        if (!(event?.type === ChatEventType.MESSAGE)) {
            return
        }
        const messageType = event.data.message_type
        const message = event.data.message
        switch (messageType) {
            case ChatMessageType.AI_MESSAGE:
                messageQueue.current.push(message);
                processMessageQueue.current()
                break
        }
    }, [lastMessage]);

    /**
     * Utility: Throttle incomming messages to keep rerenderings manageable.
     */
    const processMessageQueue = useRef(
        throttle(() => {
            const messageString = messageQueue.current.join("")
            setMessageHistory((prev) => prev.concat(messageString))
            messageQueue.current = []
        }, 100)
    );

    /**
     * Utility: Debounce to only process the final message
     */
    const processMessageHistory = useRef(
        debounce((message) => {
            setChatHistory((prev) => prev.concat({ type: ChatMessageType.AI_MESSAGE, content: message }));
            setMessageHistory(() => []);
        }, 200)
    );

    /** 
     * Function for handling the sending of messages to the chat socket.
     */
    const handleClickSendMessage = useCallback((message) => {
        let payload
        const isChatMessage = typeof message === "string"
        if (isChatMessage) {
            payload = {
                type: ChatEventType.MESSAGE,
                data: {
                    message: message,
                    message_type: ChatMessageType.HUMAN_MESSAGE
                }
            }
        } else {
            payload = {
                type: ChatEventType.MESSAGE,
                data: {
                    message: message,
                    message_type: ChatMessageType.SETTINGS
                }
            }
        }
        sendMessage(JSON.stringify(payload))
        updateStates(message)
    }, []);

    const updateStates = (message) => {
        const isChatMessage = typeof message === "string"
        if (isChatMessage) {
            if (!isDirty) {
                setIsDirty(true);
            }
            setChatHistory((prev) => prev.concat({ type: ChatMessageType.HUMAN_MESSAGE, content: message }));
        }
    }

    return [chatHistory, messageHistory, handleClickSendMessage, readyState, isDirty, settingOptions, currentSettings];
}

useChat.propTypes = {
    chatId: PropTypes.str,
}

export default useChat
