import PropTypes from 'prop-types'
import classnames from 'classnames'
import Markdown from 'react-markdown'

import { ChatMessageType } from '/src/modules/chat/hooks/useChat'


function ChatConversations({ className, chatHistory, messageHistory, ...props }) {
    const renderMessage = (message) => {
        switch (message.type) {
            case ChatMessageType.HUMAN_MESSAGE:
                return (
                    <div className="chat chat-end mb-4">
                        <div className="chat-bubble">{message.content}</div>
                    </div>
                )
            case ChatMessageType.AI_MESSAGE:
                return (
                    <Markdown>{message.content}</Markdown>
                )
        }
    }

    return (
        <div className={classnames("", className)} {...props} id="chat-conversation">

            {chatHistory?.map((message, idx) => (
                <div key={idx} className="mb-4 w-full">
                    {renderMessage(message)}
                </div>
            ))}
            {messageHistory}

        </div>
    )
}

ChatConversations.propTypes = {
    messageHistory: PropTypes.string.isRequired,
    chatHistory: PropTypes.array.isRequired,
    className: PropTypes.string,
}

export default ChatConversations
