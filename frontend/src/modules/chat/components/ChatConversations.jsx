import PropTypes from 'prop-types'
import classnames from 'classnames'
import Markdown from 'react-markdown'

import { ChatMessageType } from '/src/modules/chat/hooks/useChat'


function ChatConversations({ className, chatHistory, messageHistory, ...props }) {
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
