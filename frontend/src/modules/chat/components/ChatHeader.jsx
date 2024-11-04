import PropTypes from 'prop-types'
import classnames from 'classnames'
import { Settings } from 'lucide-react';

import { Avatar, Dropdown, Radio } from '/src/modules/common/ui-components'
import content from '/src/assets/content.json';


/**
 * ChatHeader component is used for editing chat settings and displaying the users avatar.
 */
function ChatHeader({ className, nickname, settings, currentSettings, onSettingsChange, isOnline = false, ...props }) {
    const handleChange = (event) => {
        const { name, checked, value } = event.target;
        if (checked) {
            onSettingsChange({ [name]: value })
        }
    }

    return (
        <div className={classnames('flex justify-between pb-2 bg-base-100', className)} {...props}>
            <div>
                <Dropdown
                    button={<>
                        <Settings size={20} />
                        {content.chat_settings_btn}
                    </>}
                    menu={<div className="w-32">
                        <form>
                            <p className="font-bold text-neutral-content mb-2">Model</p>
                            {settings?.models?.map((model, idx) => (
                                <Radio
                                    key={idx}
                                    checked={model.slug_name === currentSettings.model?.slug_name}
                                    onChange={handleChange}
                                    group="model"
                                    label={model.name}
                                    value={model.slug_name} />
                            ))}
                        </form>
                        <div className="divider" />
                        <form>
                            <p className="font-bold text-neutral-content mb-2">Temperature</p>
                            {settings?.temperatures?.map((temperature, idx) => (
                                <Radio key={idx}
                                    checked={temperature === currentSettings.temperature}
                                    onChange={handleChange}
                                    group="temperature"
                                    label={`${temperature}`}
                                    value={temperature} />
                            ))}
                        </form>
                    </div>}
                />
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
    onSettingsChange: PropTypes.func,
    settings: PropTypes.object,
    currentSettings: PropTypes.object,
    nickname: PropTypes.string,
    isOnline: PropTypes.bool,
    className: PropTypes.string,
}

export default ChatHeader
