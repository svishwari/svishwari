import React,{ useState } from 'react';
import { DataGrid } from '@material-ui/data-grid';
import './CTTable.scss';


//TO DO 
// ON STARRED CLICK TOGGLE FUNCTIONALITY AND API CALL
const CTTable = ({columns=[],data=[],isStarrable=true,hasImage,onStarClick,isEditing=false,children,...props}) => {
    
    const handleOnStarClick = (params) => {
        const updatedTable = [...tableData];
        console.log('i am here');
        console.log(updatedTable);
        console.log(params);
        settableData()
        onStarClick();
    }

    const starredColumn = { 
        field: 'starred', 
        headerName: ' ',
        renderCell: (params) => (
            // <span className="iconify" style={{color: params.getValue('starred') ? '#FFCD00': 'transparent',stroke: params.getValue('starred') ? 'none': '#D0D0CE'}} data-icon="mdi:star" data-inline="false"></span>
            <button onClick={()=>console.log(params)}>click me!</button>
        ),
        onCellClick: (params)=> handleOnStarClick(params),
    };

    const [tableData,settableData] = useState(data);


    const tableColumn = isStarrable ? [starredColumn,...columns] : columns;

    return (
        <span className='ct-table-wrapper'>
            <DataGrid
                // components={{
                //     NoRowsOverlay: CustomNoRowsOverlay,
                // }}
                columns={tableColumn}
                rows={tableData}
                checkboxSelection={isEditing}
                disableColumnFilter
                autoHeight
                showColumnRightBorder={false}
                hideFooterRowCount
                rowsPerPageOptions={[25]}
            />
            {children}
        </span>
    )
}

export default CTTable
