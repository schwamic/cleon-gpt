import PropTypes from 'prop-types'
import classnames from 'classnames'


function Dropdown({ className, button, menu, ...props }) {
    return (
        <div className={classnames('dropdown', className)} {...props}>
            <div tabIndex={0} role="button" className="btn btn-neutral m-1">
                {button}
            </div>
            <div
                tabIndex={0}
                className="dropdown-content card card-compact bg-neutral text-primary-content z-[1] p-2 shadow">
                <div className="card-body">
                    {menu}
                </div>
            </div>
        </div>
    )
}

Dropdown.propTypes = {
    button: PropTypes.node.isRequired,
    menu: PropTypes.node.isRequired,
    className: PropTypes.string,
}

export default Dropdown
