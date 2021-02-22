/* eslint-disable react/no-did-update-set-state */
import React, { Component } from "react";
import { DataGrid } from "@material-ui/data-grid";
import IconButton from "@material-ui/core/IconButton";
import { ReactComponent as StarEmpty } from "../../assets/icons/NotStarred.svg";
import { ReactComponent as Starred } from "../../assets/icons/Starred.svg";
import "./CTDataGrid.scss";

import CTDataGridTop from "./CTDataGridTop";

export default class CTDataGrid extends Component {
  starredColumn = {
    field: "starred",
    headerName: " ",
    width: 60,
    renderCell: (params) => {
      const updateStar = () => {
        this.updateStarring(params);
      };
      return (
        <IconButton aria-label="starring" size="small" onClick={updateStar}>
          {params.getValue("starred") ? <Starred /> : <StarEmpty />}
        </IconButton>
      );
    },
  };

  applicableColumns = this.props.hasStarring
  ? [this.starredColumn, ...this.props.columns]
  : this.props.columns;

  constructor(props) {
    super(props);
    const { data } = props;
    this.state = {
      dataGridData: data,
      isEditing: false,
      selectedRows: [],
      searchFilter: "",
    };
  }

  componentDidUpdate(nextProps) {
    const propsData = this.props.data;
    if (nextProps.data !== this.props.data) {
      this.setState({ dataGridData:  propsData});
    }
  }

  updateStarring = (params) => {
    this.updateItem(params.row.id, { starred: !params.row.starred });
  };

  onSearch = (e) => {
    this.setState({ searchFilter: e.target.value });
  };

  removeSelectedRows = () => {
    const rowsTobeRemoved = [];
    this.state.selectedRows.forEach((x) => {
      // eslint-disable-next-line eqeqeq
      const index = this.state.dataGridData.findIndex((y) => y.id == x);
      rowsTobeRemoved.push(this.state.dataGridData[index]);
    });

    const deletedArray = this.state.dataGridData.filter((value) =>
      rowsTobeRemoved.includes(value)
    );
    this.setState(prevState => ({
      dataGridData: prevState.dataGridData.filter(
        (value) => !rowsTobeRemoved.includes(value)
      ),
    }));
    this.props.onBulkRemove(deletedArray);
  };

  removeRow = (id) => {
    // eslint-disable-next-line eqeqeq
    const index = this.state.dataGridData.findIndex((x) => x.id == id);
    if (index === -1) {
      this.props.onRemove("No row found");
    } else {
      this.setState(prevState => ({
        dataGridData: [
          ...prevState.dataGridData.slice(0, index),
          ...prevState.dataGridData.slice(index + 1),
        ],
      }));
      this.props.onRemove(this.state.dataGridData[index]);
    }
  };

  toggleEditing = () => {
    this.setState(prevState=> ({ isEditing: !prevState.isEditing }) );
  };

  rowChange = (params) => {
    this.setState({ selectedRows: params.rowIds });
  };

  updateItem(id, itemAttributes) {
    const index = this.state.dataGridData.findIndex((x) => x.id === id);
    if (index !== -1) {
      this.setState(prevState => ({
        dataGridData: [
          ...prevState.dataGridData.slice(0, index),
          { ...prevState.dataGridData[index], ...itemAttributes },
          ...prevState.dataGridData.slice(index + 1),
        ],
      }));
    }
  }

  render() {
    return (
      <>
        <CTDataGridTop
          pageName={this.props.pageName}
          onSearch={this.onSearch}
          onAddClick={this.props.onAddClick}
          onDownload={this.props.onDownload}
          onRemove={this.removeSelectedRows}
          selectedRows={this.state.selectedRows}
          isEditing={this.state.isEditing}
          changeEditing={this.toggleEditing}
        />
        <DataGrid
          columns={this.applicableColumns}
          rows={this.state.dataGridData}
          checkboxSelection={this.state.isEditing}
          disableColumnFilter
          autoHeight
          disableColumnMenu
          showColumnRightBorder={false}
          disableColumnSelector
          rowHeight={60}
          headerHeight={28}
          filterModel={{
            items: [
              {
                columnField: this.props.columns[0].field,
                value: this.state.searchFilter,
                operatorValue: "contains",
              },
            ],
          }}
          onSelectionChange={(params) => this.rowChange(params)}
          //* ****************
          // TO DO THIS CAN HELP IN FUNCTIONALITY
          // onCellClick={(param)=>console.log(param)}
          //* *******************
          hideFooterRowCount
          scrollbarSize={0}
          // disableExtendRowFullWidth={true}
          hideFooter
          disableSelectionOnClick
          rowsPerPageOptions={[25]}
          className="ct-table-wrapper"
          loading={this.props.loading}
        />
      </>
    );
  }
}
