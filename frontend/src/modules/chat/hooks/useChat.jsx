import { useState, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types'
import { useConversationSocket, useListConfigurationOptions, useGetConversation } from '/src/modules/common/clients/useCleonApi';


export const ChatEventType = {
    STATUS: "status",
    MESSAGE: "message",
    AI_MESSAGE: "ai_message",
    HUMAN_MESSAGE: "human_message",
    ERROR: "error"
}

export const ChatMessageType = {
    HUMAN_MESSAGE: "human_message",
    AI_MESSAGE: "ai_message",
}

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

    useEffect(() => {
        if (lastMessage !== null) {
            const event = JSON.parse(lastMessage.data)
            var message = ""
            switch (event?.type) {
                case ChatEventType.STATUS:
                    if (event?.data?.eventType === "update_settings") {
                        getConversation()
                    } else {
                        message = messageHistory.join("")
                        setChatHistory((prev) => prev.concat({ type: "ai_message", content: message }));
                        setMessageHistory([]);
                    }
                    break
                case ChatEventType.MESSAGE:
                case ChatEventType.AI_MESSAGE:
                case ChatEventType.HUMAN_MESSAGE:
                    message = event?.data?.message
                    setMessageHistory((prev) => prev.concat(message));
                    break
                case ChatEventType.ERROR:
                    break
            }
        }
    }, [lastMessage]);

    const handleClickSendMessage = useCallback((message) => {
        var payload
        if (typeof message === "string") {
            if (!isDirty) {
                setIsDirty(true);
            }
            payload = {
                type: "human_message",
                data: {
                    message: message
                }
            }
            setChatHistory((prev) => prev.concat({ type: "human_message", content: message }));
        } else {
            payload = {
                type: "update_settings",
                data: message
            }
        }
        sendMessage(JSON.stringify(payload))
    }, [sendMessage, isDirty]);


    return [chatHistory, messageHistory, handleClickSendMessage, readyState, isDirty, settingOptions, currentSettings];
}

useChat.propTypes = {
    chatId: PropTypes.str,
}

export default useChat
