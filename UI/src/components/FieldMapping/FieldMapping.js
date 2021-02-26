import React, { useState } from 'react';
import { withStyles } from '@material-ui/core/styles';
import { Table, TableHead, TableRow, TableCell, TableBody, Fab, Button } from '@material-ui/core';
import CTInput from '../Input/CTInput';
import CTPopover from '../Popover/CTPopover';

const FieldMapping = withStyles((theme) => ({
  heading: {
    fontFamily: theme.boldFont,
    fontSize: 12,
    lineHeight: '16px',
    letterSpacing: 0.2,
  },
  cta: {
    width: 20,
    minHeight: 20,
    height: 20,
    backgroundColor: theme.colors.secondary.green,
    color: theme.colors.secondary.white,
    '&:hover, &:focus': {
      backgroundColor: theme.colors.secondary.green,
      color: theme.colors.secondary.white,
    },
  },
}))(({ classes, ...props }) => {
  const [rows] = useState([]);
  //   const createNewField = (name, mappingField) => {
  //     const newItem = { fieldName: name, mappingField };
  //     setState((prevState) => {
  //       [...prevState, newItem];
  //     });
  //   };
  return (
    <div>
      <label className={classes.heading}>{props.title}</label>
      <Table className={classes.table} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell width="200">Field Type</TableCell>
            <TableCell>Name of the Field</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.length > 0 ? (
            rows.map((row) => (
              <TableRow key={row.name}>
                <TableCell scope="row">
                  {row.fieldName}
                </TableCell>
                <TableCell>
                  <CTInput placeholder="Password / Key" value={row.mappingField} />
                </TableCell>
              </TableRow>
            ))
          ) : (
            <span>You have none selected</span>
          )}
        </TableBody>
      </Table>
      <CTPopover
        popoverContent={
          props.fields && props.fields.length > 0 ? (
            props.fields.map((field) => (
              <Button key={`${Math.random().toString(36).substr(2, 36)}`}>{field}</Button>
            ))
          ) : (
            <>{props.fields}</>
          )
        }
      >
        <>
          <Fab
            size="small"
            color="primary"
            className={classes.cta}
            disableFocusRipple
            disableRipple
          >
            <span className="iconify" data-icon="mdi:plus" data-inline="false" />
          </Fab>
          <span>Add Field Type</span>
        </>
      </CTPopover>
    </div>
  );
});

export default FieldMapping;
