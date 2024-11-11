import PropTypes from 'prop-types'
import classnames from 'classnames'
import Markdown from 'react-markdown'

import { ChatMessageType } from '/src/modules/chat/hooks/useChat'


/**
 * ChatConversations component is used to display chat messages in the chat.
 * - HUMAN_MESSAGE is displayed in a chat bubble.
 * - AI_MESSAGE is displayed as markdown.
 */
function ChatConversations({ className, chatHistory, messageChunks, ...props }) {
    return (
        <div className={classnames("", className)} {...props} id="chat-conversation">
            {chatHistory?.map((message, idx) => (
                <div key={idx} className="mb-4 w-full">
                    {message.type === ChatMessageType.HUMAN_MESSAGE ? (
                        <div className="chat chat-end mb-4">
                            <div className="chat-bubble">{message.content}</div>
                        </div>
                    ) : null}
                    {message.type === ChatMessageType.AI_MESSAGE ? (
                        <Markdown>{message.content}</Markdown>
                    ) : null}
                </div>
            ))}
            <Markdown>{messageChunks.join("")}</Markdown>
        </div>
    )
}

ChatConversations.propTypes = {
    messageChunks: PropTypes.array.isRequired,
    chatHistory: PropTypes.array.isRequired,
    className: PropTypes.string,
}

export default ChatConversations
