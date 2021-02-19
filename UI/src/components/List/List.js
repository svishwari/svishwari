import { classnames, DataGrid } from "@material-ui/data-grid";
import React from "react";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  root: {
    background: "#FFFFFF",
    boxShadow: "0px 0px 10px 2px rgba(0, 0, 0, 0.05)",
    borderRadius: "5px",
  },
}));

const CTList = (props) => {
  const classes = useStyles();
  return (
    <DataGrid
      disableColumnFilter={true}
      autoHeight={true}
      disableColumnMenu={true}
      showColumnRightBorder={false}
      disableColumnSelector={true}
      rowHeight={60}
      headerHeight={28}
      {...props}
      className={classes.root}
      hideFooter={true}
      disableSelectionOnClick={true}
    ></DataGrid>
  );
};
export default CTList;
