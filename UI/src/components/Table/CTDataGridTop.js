import React from 'react';
// import Button from '@material-ui/core/Button'; 
import CTPrimaryButton from '../Button/CTPrimaryButton';
import Input from '@material-ui/core/Input';
import './CTDataGridTop.scss';


//TO DO ITEMS CHANGE FILTER COMPONENT
const CTDataGridTop = ({pageName='Audience',isEditing=false,...props}) => {
    return (
        <div className='ct-grid-top-wrapper'>
            <span className='ct-grid-top-left'>
                <span className='iconify ct-grid-search' data-icon="mdi:search" data-inline="false"></span>
                <input className='ct-grid-search-input' placeholder='Search'></input>
            </span>
            <span className='ct-grid-top-right'>
                <span className='ct-grid-icon-buttons'>
                    {isEditing 
                    ? (<>
                        <button>
                            <span className="iconify" data-icon="mdi:download" data-inline="false"></span>
                        </button>
                        <button>
                            <span className="iconify" data-icon="mdi:delete" data-inline="false"></span>
                            <span className="ct-grid-remove-text">Remove</span>
                        </button>
                    </>
                    )
                    : (<>
                        <button>
                            <span className="iconify" data-icon="mdi:pencil" data-inline="false"></span>
                        </button>
                    </>)
                    }
                    <button>
                        <span className="iconify" data-icon="mdi:filter" data-inline="false"></span>
                    </button>
                </span>
                <CTPrimaryButton>
                    {
                        isEditing 
                        ? 'Done & Return'
                        : `+ ${pageName}`
                    }
                </CTPrimaryButton>
            </span>
        </div>
    )
}

export default CTDataGridTop
