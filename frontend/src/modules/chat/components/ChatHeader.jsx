import PropTypes from 'prop-types'
import classnames from 'classnames'
import { Plus } from 'lucide-react';

import { Avatar } from '/src/modules/common/ui-components'
import content from '/src/assets/content.json';


function ChatHeader({ className, nickname, isOnline = false, ...props }) {
    return (
        <div className={classnames('flex justify-between pb-2 bg-base-100', className)} {...props}>
            <div>
                <button type="button" className="btn btn-neutral" disabled>
                    <Plus size={20} />
                    {content.new_chat_btn}
                </button>
            </div>
            <div className="relative">
                <Avatar isOnline={isOnline} />
                <div className="absolute top-0.5 right-16">
                    <p className="font-bold">{nickname}</p>
                </div>

            </div>
        </div>
    )
}

ChatHeader.propTypes = {
    nickname: PropTypes.string,
    isOnline: PropTypes.bool,
    className: PropTypes.string,
}

export default ChatHeader
