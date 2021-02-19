import React from 'react';
import CTPrimaryButton from '../Button/CTPrimaryButton';
import './CTDataGridTop.scss';
import CTFilter from '../Filter/CTFilter';

//TO DO ITEMS CHANGE FILTER COMPONENT
const CTDataGridTop = ({onSearch,onAddClick,onRemove,onDownload,selectedRows,pageName='Audience',changeEditing,isEditing=false,...props}) => {

    return (
        <div className='ct-grid-top-wrapper'>
            <span className='ct-grid-top-left'>
                <span className='iconify ct-grid-search' data-icon="mdi:search" data-inline="false"></span>
                <input onChange={(e)=> {onSearch(e)}} className='ct-grid-search-input' placeholder='Search'></input>
            </span>
            <span className='ct-grid-top-right'>
                <span className='ct-grid-icon-buttons'>
                    {isEditing 
                    ? (<>
                        <button onClick={()=> onDownload(selectedRows) }>
                            <span className="iconify" data-icon="mdi:smile" data-inline="false"></span>
                        </button>
                        <button onClick={()=> onRemove(selectedRows) }>
                            <span className="iconify" data-icon="mdi:delete" data-inline="false"></span>
                            <span className="ct-grid-remove-text">Remove</span>
                        </button>
                    </>
                    )
                    : (<>
                        <button onClick={()=> changeEditing()}>
                            <span className="iconify" data-icon="mdi:pencil" data-inline="false"></span>
                        </button>
                    </>)
                    }
                    <button>
                        <CTFilter />
                    </button>
                </span>
                {
                    isEditing 
                        ? (<CTPrimaryButton onClick={()=> changeEditing()}>
                                Done &amp; Return
                            </CTPrimaryButton>)
                        : (<CTPrimaryButton onClick={()=>onAddClick()}>
                            {`+ ${pageName}`}
                            </CTPrimaryButton>)
                }
                

            </span>
        </div>
    )
}

export default CTDataGridTop
