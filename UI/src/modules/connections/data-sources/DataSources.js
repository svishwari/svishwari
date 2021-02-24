import React from "react";
import { connect, useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import Select from "@material-ui/core/Select";
import CTDataGrid from "../../../components/Table/CTDataGrid";
import {
  fetchDataSources,
  triggerIngestion,
  triggerConnectionCheck,
  addNewDataSource,
} from "../store/action";
import CTModal from "../../../components/Modal/CTModal";
import CTLabel from "../../../components/Label/CTLabel";
import CTInput from "../../../components/Input/CTInput";
import CTChip from "../../../components/Chip/CTChip";
import "./DataSource.scss";

const markIngestionStatus = (payload) => ({
  type: "updateInestionStatus",
  payload,
});
const markConnecting = (payload) => ({
  type: "updateConnectionStatus",
  payload,
});

const DataSources = (props) => {
  // this hook allows us to access the dispatch function
  const dispatch = useDispatch();
  const columns = [
    {
      field: "fileName",
      headerName: "File Name",
      flex: 0.2,
      renderCell: (params) => (
        <Link to={() => false}>
          {params.getValue("fileName")}{" "}
          <span
            className="iconify"
            data-icon="mdi:open-in-new"
            data-inline="false"
          />
        </Link>
      ),
    },
    {
      field: "source",
      headerName: "Source",
      flex: 0.1,
    },
    {
      field: "lastUpdated",
      headerName: "Last Updated",
      flex: 0.15,
    },
    {
      field: "connectionStatus",
      headerName: "Connection Status",
      flex: 0.15,
      renderCell: (params) => {
        const triggerConnection = () => {
          const payload = {
            id: params.getValue("id"),
            status: "Connecting...",
          };
          dispatch(markConnecting(payload));
          initiateConnection(params.getValue("id"));
        };
        return (
          <>
            {params.getValue("connectionStatus") !== "Connecting..." ? (
              <CTChip
                hasIcons
                isWorking={params.getValue("connectionStatus") === "Connected"}
                isWorkingFn={triggerConnection}
                isNotWorkingFn={triggerConnection}
              >
                {params.getValue("connectionStatus")}
              </CTChip>
            ) : (
              <span>Connecting...</span>
            )}
          </>
        );
      },
    },
    {
      field: "recordsIngested",
      headerName: "Ingested",
      flex: 0.15,
      renderCell: (params) => {
        const triggerDataIngestion = () => {
          const payload = {
            id: params.getValue("id"),
            status: "Ingestion in Progress...",
          };
          dispatch(markIngestionStatus(payload));
          actionIngestion(params.getValue("id"));
        };
        if(params.getValue("connectionStatus") !== "Connected"){
          return <></>;
        }
        if( !params.getValue("ingested") &&  params.getValue("ingestionStatus") !== "InProgess")  {
          return (
              <CTChip
                hasIcons
                isWorking={params.getValue("ingested")}
                isWorkingFn={() => triggerDataIngestion(params)}
                isNotWorkingFn={() => triggerDataIngestion(params)}
              >
                Not ingested
              </CTChip>
          );
        }
        if( !params.getValue("ingested") &&  params.getValue("ingestionStatus") === "InProgess") {
          return (<span>Ingestion in progress...</span>);
        }
        if ( params.getValue("ingested") ) {
          return (<span>{params.getValue("recordsIngested")}</span>);
        }
        return (<></>);
      },
    },
    {
      field: "empty",
      headerName: "Empty",
      flex: 0.1,
      renderCell: (params) =>
        params.getValue("connectionStatus") === "Connected" && 
        params.getValue("ingested") && 
        params.getValue("ingestionStatus") !== "InProgess" ? (
          params.getValue("recordsIngested")
        ) : (
          <></>
        ),
    },
    {
      field: "bogus",
      headerName: "Bogus",
      flex: 0.1,
      renderCell: (params) =>
        params.getValue("connectionStatus") === "Connected" && 
        params.getValue("ingested") && 
        params.getValue("ingestionStatus") !== "InProgess" ? (
          params.getValue("recordsIngested")
        ) : (
          <></>
        ),
    },
    {
      field: "cleansed",
      headerName: "Cleansed",
      flex: 0.1,
      renderCell: (params) =>
        params.getValue("connectionStatus") === "Connected" && 
        params.getValue("ingested") && 
        params.getValue("ingestionStatus") !== "InProgess" ? (
          params.getValue("recordsIngested")
        ) : (
          <></>
        ),
    },
  ];

  const retrieveDataSources = () => {
    dispatch(fetchDataSources());
  };
  const actionIngestion = (id) => {
    dispatch(triggerIngestion(id));
  };
  const initiateConnection = (id) => {
    dispatch(triggerConnectionCheck(id));
  };
  React.useEffect(() => {
    retrieveDataSources();
  }, []);
  const [selectedDataSource, setselectedDataSource] = React.useState(
    "Amazon S3"
  );
  const handleSelectedDataSourceChange = (event) => {
    setselectedDataSource(event.target.value);
  };
  const addDataSourceContent = (
    <div className="ct-datasource-modal">
      <CTLabel>Data Source</CTLabel>
      <Select
        value={selectedDataSource}
        onChange={(e) => handleSelectedDataSourceChange(e)}
        label="Account ID"
        className="ct-datasource-modal-select"
      >
        <option value="Amazon S3">Amazon S3</option>
        <option value="CDP">CDP</option>
        <option value="Facebook">Facebook</option>
      </Select>

      {selectedDataSource === "Amazon S3" ? (
        <div className="ct-datasource-fields">
          <span className="ct-datasource-field-card">
            <CTLabel>IAM User Name</CTLabel>
            <CTInput placeholder="IAM User Name" />
          </span>
          <span className="ct-datasource-field-card">
            <CTLabel>Password / Key</CTLabel>
            <CTInput placeholder="Password / Key" />
          </span>
          <span className="ct-datasource-field-card">
            <CTLabel>Filename</CTLabel>
            <CTInput placeholder="Unique name for your file" />
          </span>
          <span className="ct-datasource-field-card">
            <CTLabel>Filepath</CTLabel>
            <CTInput placeholder="example.csv" />
          </span>
        </div>
      ) : (
        ""
      )}
      {selectedDataSource === "Facebook" ? (
        <div className="ct-datasource-fields">
          <span className="ct-datasource-field-card">
            <CTLabel>IAM User Name</CTLabel>
            <CTInput placeholder="IAM User Name" />
          </span>
          <span className="ct-datasource-field-card">
            <CTLabel>Password / Key</CTLabel>
            <CTInput placeholder="Password / Key" />
          </span>
          <span className="ct-datasource-field-card">
            <CTLabel>Filename</CTLabel>
            <CTInput placeholder="Unique name for your file" />
          </span>
        </div>
      ) : (
        ""
      )}
      {selectedDataSource === "CDP" ? (
        <div className="ct-datasource-fields">
          <span className="ct-datasource-field-card">
            <CTLabel>IAM User Name</CTLabel>
            <CTInput placeholder="IAM User Name" />
          </span>
          <span className="ct-datasource-field-card">
            <CTLabel>Password / Key</CTLabel>
            <CTInput placeholder="Password / Key" />
          </span>
        </div>
      ) : (
        ""
      )}
    </div>
  );
  const childRef = React.useRef();

  return (
    <>
      <CTDataGrid
        data={props.dataSources}
        columns={columns}
        hasStarring
        loading={!props.dataSources.length}
        onAddClick={() => {
          childRef.current.handleOpen();
        }}
        pageName="Data Source"
        isTopVisible
        isSummaryEnabled
        bulkOperationText="Ingest Selected"
        summaryContent={[
          {value: "52",title: "Total Data Sources"},
          {value: "24",title: "Ingested Records"},
          {value: "34",title: "Empty"},
          {value: "600",title: "Errors"},
          {value: "4",title: "Cleansed"},
          {value: "1.3",decimals:"1",suffix: "k",title: "Stitched"},
          {value: "1.4",decimals:"1",suffix: "k",title: "Pinned"},
        ]}
        moreIconContent={[
          {name: "Configure", function: ()=> {} },
        ]}
        enableMoreIcon
      />
      <CTModal
        ref={childRef}
        modalTitle="Add Data Source"
        modalSubtitle="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        modalBody={addDataSourceContent}
        mainCTAText="Verify and Add"
        onComplete={() => dispatch(addNewDataSource())}
      />
    </>
  );
};
const mapStateToProps = (state) => ({
  dataSources: state.connections.dataSources || [],
});
export default connect(mapStateToProps)(DataSources);
