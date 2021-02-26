import React from "react";
import { connect, useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import CTDataGrid from "../../../components/Table/CTDataGrid";
import {
  fetchDataSources,
  triggerIngestion,
  triggerConnectionCheck,
} from "../store/action";
import CTChip from "../../../components/Chip/CTChip";
import "./DataSource.scss";

import { showAddDataSource } from "../../modal/action";


const FILTER_TYPES = {
  "Starred": {
    selectMultiple: false,
    values: ["Starred", "Not Starred"]
  },
  "Connection Status": { 
    selectMultiple: true,
    values: ["Connected", "Not Connected"]
  },
  "Source": {
    selectMultiple: false,
    values: ["Client", "Amazon S3"]
  }
}

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
                onClickFunc={triggerConnection}
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
                onClickFunc={() => triggerDataIngestion(params)}
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

  return (
    <>
      <CTDataGrid
        data={props.dataSources}
        columns={columns}
        hasStarring
        loading={!props.dataSources.length}
        pageName="Data Source"
        isTopVisible
        isSummaryEnabled
        onAddClick={()=> dispatch(showAddDataSource())}
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
        filterTypes={FILTER_TYPES}
        moreIconContent={[
          {name: "Configure", function: ()=> {} },
        ]}
        enableMoreIcon
      />
    </>
  );
};
const mapStateToProps = (state) => ({
  dataSources: state.connections.dataSources || [],
});
export default connect(mapStateToProps)(DataSources);
