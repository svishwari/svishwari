import React from 'react';
import { Chip, IconButton } from "@material-ui/core";
import './CTChip.scss';

const CTChip = ({params,isDeliverabe=true,...props}) => {
    return (
        <div className='ct-chip-wrapper'>
            <Chip 
                label={params.getValue("status")} 
                className={`${(params.getValue("delivered") === true) ? 'ct-chip-delivered' : 'ct-chip-not-delivered'}`}
            />
            { isDeliverabe 
            ? 
                (params.getValue("delivered") === true 
                ? 
                    (<IconButton {...props}>
                        <span
                        className="iconify ct-chip-delivered-icon"
                        data-icon="mdi:refresh-circle"
                        data-inline="false"
                        ></span>
                    </IconButton>) 
                : 
                (<IconButton {...props}>
                    <span
                    className="iconify ct-chip-not-delivered-icon"
                    data-icon="mdi:arrow-right-circle"
                    data-inline="false"
                    ></span>
                </IconButton>)
                )
            : 
            (<></>)
            }
      </div>
    )
}

export default CTChip
