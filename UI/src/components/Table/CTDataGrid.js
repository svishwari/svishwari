import React, { Component } from "react";
import { DataGrid } from "@material-ui/data-grid";
import IconButton from "@material-ui/core/IconButton";
import { ReactComponent as StarEmpty } from '../../assets/icons/NotStarred.svg';
import { ReactComponent as Starred } from '../../assets/icons/Starred.svg';
import './CTDataGrid.scss'

export default class CTDataGrid extends Component {
  constructor(props) {
    super(props);
    const { data } = props;
    this.state = {
      dataGridData: data,
      isEditing: this.props.isEditing,
    };
    // this.setState({ dataGridData: this.props.data });
  }
  updateItem(id, itemAttributes) {
    var index = this.state.dataGridData.findIndex((x) => x.id === id);
    if (index === -1) {
    } else
      this.setState({
        dataGridData: [
          ...this.state.dataGridData.slice(0, index),
          Object.assign({}, this.state.dataGridData[index], itemAttributes),
          ...this.state.dataGridData.slice(index + 1),
        ],
      });
  }

  updateStarring = (params) => {
    //   console.log(params.row.id)
    this.updateItem(params.row.id, { starred: !params.row.starred });
    // this.setState({ dataGridData: this.dataGridData });
  };

  starredColumn = {
    field: "starred",
    headerName: " ",
    width: 60,
    renderCell: (params) => {
      const updateStar = () => {
        console.log(params);
        this.updateStarring(params);
      };
      return (
        <IconButton aria-label="starring" size="small" onClick={updateStar}>
          {params.getValue("starred") ? <Starred/>: <StarEmpty/>}
        </IconButton>
      );
    },
  };
  applicableColumns = this.props.hasStarring
    ? [this.starredColumn, ...this.props.columns]
    : this.props.columns;
  render() {
    return (
      <>
        <DataGrid
          columns={this.applicableColumns}
          rows={this.state.dataGridData}
          checkboxSelection={true}
          disableColumnFilter={true}
          autoHeight={true}
          disableColumnMenu={true}
          showColumnRightBorder={false}
          disableColumnSelector={true}
          rowHeight={60}
          headerHeight={28}
          //*****************
          // TO DO THIS CAN HELP IN FUNCTIONALITY
          // onCellClick={(param)=>console.log(param)}
          //********************
          hideFooterRowCount={true}
          scrollbarSize={0}
          // disableExtendRowFullWidth={true}
          hideFooter={true}
          disableSelectionOnClick={true}
          rowsPerPageOptions={[25]}
          className="ct-table-wrapper"
        />
      </>
    );
  }
}
