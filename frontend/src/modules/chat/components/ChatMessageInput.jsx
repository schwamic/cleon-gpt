import PropTypes from 'prop-types'
import { useState } from 'react'
import classnames from 'classnames'
import { Send } from 'lucide-react';

import content from '/src/assets/content.json';

/**
 * ChatMessageInput component is a textarea input for sending messages in the chat.
 */
function ChatMessageInput({ className, disabled = false, onClick, ...props }) {
    const [text, setText] = useState('');

    const updateText = (event) => {
        setText(event.target.value);
    }

    const sendText = () => {
        onClick(text);
        setText('');
    }

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendText();
        }
    }

    return (
        <div className={classnames('relative', className)} {...props}>
            <label className="form-control">
                <textarea
                    placeholder={content.message_input_placeholder}
                    disabled={disabled}
                    className="textarea textarea-bordered textarea-sm w-full resize-y min-h-16 sm:min-h-32"
                    value={text}
                    onChange={updateText}
                    onKeyDown={handleKeyDown}
                />
                <div className="label">
                    <span className="label-text-alt">{content.gpt_warning}</span>
                    <span className="label-text-alt">{content.chat_input_info}</span>
                </div>
            </label>
            <div className="absolute right-2 bottom-10 inline-block">
                <button type="button" className="btn btn-square btn-neutral" disabled={disabled} onClick={sendText}>
                    <Send size={20} />
                </button>
            </div>
        </div>
    )
}

ChatMessageInput.propTypes = {
    onClick: PropTypes.func.isRequired,
    disabled: PropTypes.bool,
    className: PropTypes.string,
}

export default ChatMessageInput
