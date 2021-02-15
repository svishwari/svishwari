import React, {useState} from 'react';
import Toast from 'react-bootstrap/Toast';
import './CTToast.scss';

const CTToast = ({
        showToast=true,
        autoHide=false,
        autoHideTime=3000,
        toastType='success',
        toastMessage='',
        ...props
    }) => {
    const [show, setShow] = useState(showToast);

    return (
        <Toast 
            show={show} 
            delay={autoHideTime} 
            autohide={autoHide} 
            className={`ct-toast-wrapper`}
            onClose={() => setShow(false)}
            {...props}
        >
            <div className={`ct-toast-inner-wrapper ${(toastType==='success') ? 'ct-toast-success': 'ct-toast-error'}`}>
                <div className='left-section'>
                    { toastType==='success' ? 
                        <span className="iconify" data-icon="mdi:emoticon-happy" data-inline="false"></span>
                        : <span className="iconify" data-icon="mdi:alert-octagram" data-inline="false"></span>
                    }
                    <div className='ct-toast-message'>
                        {toastMessage}
                    </div>
                </div>
                <div className='right-section' onClick={()=>setShow(false)}>
                    { (autoHide===false) ?
                        <span className="iconify" data-icon="zmdi:close" data-inline="false"></span>
                        : 
                        <></>
                    }
                </div>
            </div>
        </Toast>
    )
}

export default CTToast
