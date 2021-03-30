import { DataGrid } from "@material-ui/data-grid";
import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import "./List.scss";

const useStyles = makeStyles(() => ({
  root: {
    background: "#FFFFFF",
    borderRadius: "5px",
  },
}));

const CTList = (props) => {
  const classes = useStyles();
  return (
    <DataGrid
      disableColumnFilter
      autoHeight
      disableColumnMenu
      showColumnRightBorder={false}
      disableColumnSelector
      rowHeight={60}
      headerHeight={props.headerHeight || 0}
      {...props}
      className={`${classes.root} ct-list-wrapper`}
      hideFooter
      disableSelectionOnClick
    />
  );
};
export default CTList;
