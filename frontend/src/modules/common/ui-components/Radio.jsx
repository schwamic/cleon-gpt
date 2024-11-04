import PropTypes from 'prop-types'
import classnames from 'classnames'

function Radio({ className, label, value, group, checked, onChange, ...props }) {
    return (
        <label className="label cursor-pointer" {...props}>
            <span className="label-text">{label}</span>
            <input
                type="radio"
                name={group}
                value={value}
                className={classnames("radio", className)}
                checked={checked}
                onChange={onChange} />
        </label>
    )
}

Radio.propTypes = {
    label: PropTypes.string,
    value: PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.number
    ]),
    group: PropTypes.string,
    className: PropTypes.string,
    checked: PropTypes.bool,
    onChange: PropTypes.func,
}

export default Radio
