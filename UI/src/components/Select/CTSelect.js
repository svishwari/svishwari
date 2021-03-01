import React, { useState } from 'react';
import Select from "@material-ui/core/Select";
import "./CTSelect.scss";

const CTSelect = ({selectOptions=[],selectLabel="label",onChange,defaultValue,...props}) => {
    const initialValue = defaultValue || selectOptions[0];
    const [selectedValue, setselectedValue] = useState(initialValue);
    const onValueChange = (e) => {
        setselectedValue(e.target.value);
        onChange(e);
    }
    
    return (
        <Select
            value={selectedValue}
            onChange={(e) => onValueChange(e)}
            label={selectLabel}
            className="ct-select-wrapper"
            {...props}
        >
            {
                selectOptions.map(value=>(
                    <option key={value} value={value}>{value}</option>
                ))
            }  
        </Select>
    )
}

export default CTSelect
