import { useState, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types'
import { useConversationSocket } from '/src/modules/common/clients/useCleonApi';


export const ChatEventType = {
    STATUS: "status",
    MESSAGE: "message"
}

export const ChatMessageType = {
    HUMAN_MESSAGE: "human_message",
    AI_MESSAGE: "ai_message",
}

function useChat(userId) {
    const [messageHistory, setMessageHistory] = useState([]);
    const [chatHistory, setChatHistory] = useState([]);
    const { sendMessage, lastMessage, readyState } = useConversationSocket(userId);
    const [isDirty, setIsDirty] = useState(false);

    useEffect(() => {
        if (lastMessage !== null) {
            const event = JSON.parse(lastMessage.data)
            if (event?.type == ChatEventType.STATUS) {
                const message = messageHistory.join("")
                setChatHistory((prev) => prev.concat({ type: "ai_message", content: message }));
                setMessageHistory([]);
            } else {
                const message = event?.data?.message
                setMessageHistory((prev) => prev.concat(message));
            }
        }
    }, [lastMessage]);

    const handleClickSendMessage = useCallback((prompt) => {
        if (!isDirty) {
            setIsDirty(true);
        }
        setChatHistory((prev) => prev.concat({ type: "human_message", content: prompt }));
        const message = {
            type: "human_message",
            data: {
                message: prompt
            }
        }
        sendMessage(JSON.stringify(message))
    }, [sendMessage, isDirty]);


    return [chatHistory, messageHistory, handleClickSendMessage, readyState, isDirty];
}

useChat.propTypes = {
    userId: PropTypes.str,
}

export default useChat
