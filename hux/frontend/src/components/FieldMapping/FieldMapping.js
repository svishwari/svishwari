import React, { useState } from 'react';
import { Table, TableHead, TableRow, TableCell, TableBody } from '@material-ui/core';
import CTInput from '../Input/CTInput';
import CTPopover from '../Popover/CTPopover';
import CardWrapper from "../Cards/CardGroup/CTCardGroup"
import "./FieldMapping.scss";

const FieldMapping = (( props) => {
  const [rows,setRows] = useState([]);
  const [fields, setFields] = useState(props.fields);

  const createNewField = (name, mappingField="") => {
    const newItem = { fieldName: name, mappingField };
    setRows([newItem,...rows]);
    const newField = fields.filter(each=> each!==name);
    setFields(newField);
  };

  const removeRow = (row) => {
    setFields([row.fieldName,...fields]);
    const newRows = rows.filter(each=> each.fieldName!==row.fieldName);
    setRows(newRows);
  };

  const popoverContent = fields ? (
    <div className="field-mapping-popover">
      <div className="field-mapping-popover-title">ADD</div>
      {
        fields.map((field) => (
          <div className="field-mapping-popover-type" key={field} onKeyPress={()=> createNewField(field)} onClick={()=> createNewField(field)}>
            {field}
          </div>
        ))
      }
    </div>
  ) : (
    <>{fields}</>
  )

  return (
    <div className="field-mapping-wrapper">
      <div className="add-field-container">
        <CTPopover
          popoverContent={popoverContent}
        >
          <span className="add-field-icon">
              <span className="iconify" data-icon="mdi:plus-circle" data-inline="false" />
          </span>
        </CTPopover>
        <span className="add-field-text">Add Field Type</span>
      </div>
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
                  <CardWrapper>
                    <CTInput />
                    <span onClick={()=> removeRow(row)} onKeyPress={()=> removeRow(row)} className="field-mapping-delete">
                      <span className="iconify" data-icon="mdi:delete" data-inline="false" />
                    </span>
                  </CardWrapper>
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
    </div>
  );
});

export default FieldMapping;
