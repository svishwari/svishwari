import React, { Component } from "react";
import { DataGrid } from "@material-ui/data-grid";
import IconButton from "@material-ui/core/IconButton";
import { ReactComponent as StarEmpty } from '../../assets/icons/NotStarred.svg';
import { ReactComponent as Starred } from '../../assets/icons/Starred.svg';
import './CTDataGrid.scss';

import CTDataGridTop from './CTDataGridTop';

export default class CTDataGrid extends Component {
  constructor(props) {
    super(props);
    const { data } = props;
    this.state = {
      dataGridData: data,
      isEditing: false,
      selectedRows: [],
      searchFilter: '',
    };
  }
  updateItem(id, itemAttributes) {
    let index = this.state.dataGridData.findIndex((x) => x.id === id);
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
  componentDidUpdate(nextProps) {
    const { data } = this.props
    if (nextProps.data !== this.props.data) {
      this.setState({ dataGridData: this.props.data })
    }
  }
  updateStarring = (params) => {
    //   console.log(params.row.id)
    this.updateItem(params.row.id, { starred: !params.row.starred });
    // this.setState({ dataGridData: this.dataGridData });
  };

  toggleEditing = () => {
    this.setState({isEditing: !this.state.isEditing});
  }

  rowChange = (params) => {
    this.setState({selectedRows: params.rowIds});
  }

  removeRow = (id) => {
    let index = this.state.dataGridData.findIndex((x) => x.id == id);
    if (index === -1) {
      this.props.onRemove('No row found');
    } else{
      let updatedArray = [
        ...this.state.dataGridData.slice(0, index),
        ...this.state.dataGridData.slice(index + 1),
      ];
      this.setState({
        dataGridData: updatedArray,
      });
      this.props.onRemove(this.state.dataGridData[index]);
    }
  }

  removeSelectedRows = () => {
    let rowsTobeRemoved = []
    this.state.selectedRows.forEach( x =>{
      let index = this.state.dataGridData.findIndex((y) => y.id == x);
      rowsTobeRemoved.push(this.state.dataGridData[index]);
    })

    let filteredArray = this.state.dataGridData.filter(value => !rowsTobeRemoved.includes(value));
    let deletedArray = this.state.dataGridData.filter(value => rowsTobeRemoved.includes(value));
    this.setState({
      dataGridData: filteredArray
    })
    this.props.onBulkRemove(deletedArray);
  }

  onSearch = (e) => {
    this.setState({searchFilter: e.target.value})
  }

  starredColumn = {
    field: "starred",
    headerName: " ",
    width: 60,
    renderCell: (params) => {
      const updateStar = () => {
        // console.log(params);
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
        <CTDataGridTop pageName={this.props.pageName} onSearch={this.onSearch} onAddClick={this.props.onAddClick} onDownload={this.props.onDownload} onRemove={this.removeSelectedRows} selectedRows={this.state.selectedRows} isEditing={this.state.isEditing} changeEditing={this.toggleEditing}></CTDataGridTop>
        <DataGrid
          columns={this.applicableColumns}
          rows={this.state.dataGridData}
          checkboxSelection={this.state.isEditing}
          disableColumnFilter={true}
          autoHeight={true}
          disableColumnMenu={true}
          showColumnRightBorder={false}
          disableColumnSelector={true}
          rowHeight={60}
          headerHeight={28}
          filterModel={{
                items: [
                  { columnField: this.props.columns[0].field, value: this.state.searchFilter, operatorValue: 'contains' },
                ],
              }
          }
          onSelectionChange={(params)=>this.rowChange(params)}
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
          loading={this.props.loading}
        />
      </>
    );
  }
}
