import { useState, useEffect, useCallback } from 'react';
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

    useEffect(() => {
        setCurrentSettings({
            model: conversation?.model,
            temperature: conversation?.configuration?.temperature
        })
    }, [conversation]);

    /**
     * useEffect for handling incoming messages from the chat socket.
     */
    useEffect(() => {
        if (lastMessage !== null) {
            const event = JSON.parse(lastMessage.data)
            const messageType = event?.data?.message_type
            var message = ""
            switch (event?.type) {
                case ChatEventType.STATUS:
                    if (messageType === ChatMessageType.SETTINGS) {
                        getConversation()
                    }
                    else if (messageType === ChatMessageType.HUMAN_MESSAGE) {
                        message = messageHistory.join("")
                        setChatHistory((prev) => prev.concat({ type: ChatMessageType.AI_MESSAGE, content: message }));
                        setMessageHistory(() => []);
                    }
                    break
                case ChatEventType.MESSAGE:
                    if (messageType === ChatMessageType.AI_MESSAGE) {
                        message = event?.data?.message
                        setMessageHistory((prev) => prev.concat(message));
                    }
                    break
            }
        }
    }, [lastMessage]);

    /** 
     * Function for handling the sending of messages to the chat socket.
     */
    const handleClickSendMessage = useCallback((message) => {
        var payload
        if (typeof message === "string") {
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
    }, [sendMessage, isDirty]);

    const updateStates = (message) => {
        if (typeof message === "string") {
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
