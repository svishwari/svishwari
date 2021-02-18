import { classnames, DataGrid } from "@material-ui/data-grid";
import React from "react";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
}))

const CTList = (props) => {
    const classes = useStyles()
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
      hideFooter={true}
      disableSelectionOnClick={true}
    className={classes}></DataGrid>
  );
};
export default CTList;
