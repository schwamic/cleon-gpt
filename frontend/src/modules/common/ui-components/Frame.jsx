import PropTypes from 'prop-types'
import classnames from 'classnames'

function Frame({ children, className, ...props }) {
    return (
        <div
            className={classnames('min-h-screen w-screen p-4 sm:p-8 max-w-2xl mx-auto', className)}
            {...props}>
            {children}
        </div>
    )
}

Frame.propTypes = {
    children: PropTypes.node.isRequired,
    className: PropTypes.string,
}

export default Frame
