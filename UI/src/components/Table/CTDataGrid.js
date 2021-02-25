/* eslint-disable react/no-did-update-set-state */
import React, { Component } from "react";
import { DataGrid } from "@material-ui/data-grid";
import IconButton from "@material-ui/core/IconButton";
import { ReactComponent as StarEmpty } from "../../assets/icons/NotStarred.svg";
import { ReactComponent as Starred } from "../../assets/icons/Starred.svg";
import "./CTDataGrid.scss";

import CTDataGridTop from "./CTDataGridTop";
import SummaryCard from "../Cards/SummaryCard/SummaryCard";
import CTCardGroup from "../Cards/CardGroup/CTCardGroup";
import CTPopover from "../Popover/CTPopover";

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

  moreColumn = {
    field: "more",
    headerName: " ",
    renderCell: (params) => {
      const popOverContent = this.props.moreIconContent.map(content => 
          <div key={content.name} onKeyPress={() => content.function()} onClick={content.function}>{content.name}</div>
      );
      const removeItem = <div 
                    onKeyPress={() => this.removeRow(params.getValue("id"))}
                    onClick={()=>this.removeRow(params.getValue("id"))}
                    style={{cursor: "pointer"}}
                    key="remove"
                  >
                    Remove
                  </div>
      popOverContent.push(removeItem);

      return (
        <CTPopover popoverContent={popOverContent}>
          <IconButton aria-label="more" size="small">
            <span className="iconify" data-icon="mdi:dots-vertical" data-inline="false" />
          </IconButton>
        </CTPopover>
      );
    },
  };

  applicableColumns = this.props.hasStarring
  ? [this.starredColumn, ...this.props.columns]
  : this.props.columns;

  applicableColumns = this.props.enableMoreIcon
  ? [...this.applicableColumns,this.moreColumn]
  : this.applicableColumns;

  constructor(props) {
    super(props);
    const { data } = props;
    this.state = {
      dataGridData: data,
      isEditing: false,
      selectedRows: [],
      searchFilter: "",
      isSummaryVisible: false,
    };
  }

  componentDidUpdate(nextProps) {
    const propsData = this.props.data;
    if (nextProps.data !== this.props.data) {
      this.setState({ dataGridData:  propsData});
    }
  }

  onSummaryToggle = () => {
    this.setState(prevState => ({
      isSummaryVisible: !prevState.isSummaryVisible,
    }));
  };

  onBulkOperation = () => {
    const rowsTobeOperated = [];
    this.state.selectedRows.forEach((x) => {
      // eslint-disable-next-line eqeqeq
      const index = this.state.dataGridData.findIndex((y) => y.id == x);
      rowsTobeOperated.push(this.state.dataGridData[index]);
    });

    const bulkSelectedRows = this.state.dataGridData.filter((value) =>
      rowsTobeOperated.includes(value)
    );
    this.props.onBulkFunction(bulkSelectedRows);
  };

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
      { this.props.isTopVisible ?
      <>
        <CTDataGridTop
          pageName={this.props.pageName}
          isSummaryEnabled={this.props.isSummaryEnabled}
          onSearch={this.onSearch}
          onAddClick={this.props.onAddClick}
          onDownload={this.props.onDownload}
          onRemove={this.removeSelectedRows}
          selectedRows={this.state.selectedRows}
          isEditing={this.state.isEditing}
          changeEditing={this.toggleEditing}
          onSummaryToggle={this.onSummaryToggle}
          isDownloadAble={this.props.isDownloadAble}
          onBulkOperation={this.onBulkOperation}
          bulkOperationText={this.props.bulkOperationText}
        />
        {
          this.state.isSummaryVisible ? 
          <CTCardGroup style={{margin: "10px 20px"}}>
          {this.props.summaryContent.map(content =>
          <SummaryCard decimals={content.decimals} value={content.value} suffix={content.suffix} title={content.title}/>
          )}
          </CTCardGroup>
          : <></>
        }
      </>
        : <></>
      }
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
          headerHeight={this.props.headerHeight}
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

CTDataGrid.defaultProps = {
  hasStarring: false,
  columns: [],
  data: [],
  loading: false,
  isSummaryEnabled: false,
  pageName: "",
  isTopVisible: true,
  isDownloadAble: false,
  bulkOperationText: "",
  moreIconContent: [],
  enableMoreIcon: false,
  onBulkRemove: () => {},
  onRemove: () => {},
  onDownload: () => {},
  onAddClick: () => {},
  onBulkFunction: () => {}
};