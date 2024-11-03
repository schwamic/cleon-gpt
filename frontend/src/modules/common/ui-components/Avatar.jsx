import PropTypes from 'prop-types'
import classnames from 'classnames'
import monsterPortrait from '/src/assets/monster.svg'


function Avatar({ className, isOnline = false, ...props }) {
    return (
        <div className={classnames("avatar", { "online": isOnline, "offline": !isOnline }, className)} {...props}>
            <div className="w-12 mask mask-squircle bg-white p-1">
                <img className="mt-1" src={monsterPortrait} alt="Avatar picture" />
            </div>
        </div>
    )
}

Avatar.propTypes = {
    className: PropTypes.string,
    isOnline: PropTypes.bool,
}

export default Avatar
