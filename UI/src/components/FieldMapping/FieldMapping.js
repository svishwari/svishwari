import React, { useState } from 'react';
import { Table, TableHead, TableRow, TableCell, TableBody, Fab, Button } from '@material-ui/core';
import CTInput from '../Input/CTInput';
import CTPopover from '../Popover/CTPopover';
import "./FieldMapping.scss";

const FieldMapping = (( props) => {
  const [rows,setRows] = useState([]);
  const createNewField = (name, mappingField="") => {
    const newItem = { fieldName: name, mappingField };
    setRows([...rows, newItem]);
  };

  return (
    <div className="field-mapping-wrapper">
      <div className="field-mapping-title">{props.title}</div>
      <Table aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell className="field-mapping-head" width="200">Field Type</TableCell>
            <TableCell className="field-mapping-head">Name of the Field</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.length > 0 ? (
            rows.map((row) => (
              <TableRow key={row.name}>
                <TableCell scope="row" className="field-type">
                  {row.fieldName}
                </TableCell>
                <TableCell>
                  <CTInput value={row.mappingField} />
                </TableCell>
              </TableRow>
            ))
          ) : (
            <TableRow >
                <TableCell scope="row" className="field-type">
                  You have none selected
                </TableCell>
                <TableCell>
                  <span />
                </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
      <CTPopover
        popoverContent={
          props.fields && props.fields.length > 0 ? (
            props.fields.map((field) => (
              <div>
              <Button onClick={()=> createNewField(field)} key={`${Math.random().toString(36).substr(2, 36)}`}>{field}</Button>
              </div>
            ))
          ) : (
            <>{props.fields}</>
          )
        }
      >
        <span>
          <Fab
            size="small"
            color="primary"
            disableFocusRipple
            disableRipple
          >
            <span className="iconify" data-icon="mdi:plus" data-inline="false" />
          </Fab>
        </span>
      </CTPopover>
      <span>Add Field Type</span>
    </div>
  );
});

export default FieldMapping;
