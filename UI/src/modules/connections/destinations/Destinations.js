import React from "react";
import { connect, useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import CTDataGrid from "../../../components/Table/CTDataGrid";
import CTChip from "../../../components/Chip/CTChip";

import {
  fetchDestinations,
  triggerDestinationConnectionCheck,
} from "../store/action";

import { showAddDestination } from "../../modal/action"; 

const markConnecting = (payload) => ({
  type: "updateDestinationConnectionStatus",
  payload,
});


const Destinations = (props) => {
  const dispatch = useDispatch();
  
  const retrieveDestinations = () => {
    dispatch(fetchDestinations());
  };

  React.useEffect(() => {
    retrieveDestinations()
  }, []);

  const initiateConnection = (id) => {
    dispatch(triggerDestinationConnectionCheck(id));
  };
  const columns = [
    {
      field: "destinationName",
      headerName: "Destination",
      flex: 0.2,
      renderCell: (params) => {
        const destinationLogo = params.getValue("destination")
        return (
        <>
          <span style={{marginRight: "12px"}}>
          {
            destinationLogo === "fb" ?
              <span className="iconify" data-icon="logos:facebook" data-inline="false" />
            : destinationLogo === "sfmc" ?
              <span className="iconify" data-icon="logos:salesforce" data-inline="false" />
            : destinationLogo === "ga" ?
              <span className="iconify" data-icon="grommet-icons:google" data-inline="false" />
            : <></>
          }
          </span>
          <Link to="/destinations">
            {`${params.getValue("destinationName")} `}
            <span
              className="iconify"
              data-icon="mdi:open-in-new"
              data-inline="false"
            />
          </Link>
        </>
      )},
    },
    {
      field: "accountName",
      headerName: "Account Name",
      flex: 0.1,
    },
    {
      field: "lastUpdated",
      headerName: "Last Updated",
      flex: 0.15,
    },
    {
      field: "connectionStatus",
      headerName: "Status",
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
    
  ];
  return (
    <CTDataGrid
      data={props.destinations}
      columns={columns}
      hasStarring
      loading={!props.destinations.length}
      pageName="Destination"
      isTopVisible
      headerHeight={28}
      onAddClick={()=> dispatch(showAddDestination())}
      enableMoreIcon
      moreIconContent={[
        {name: "Configure", function: ()=> {} },
      ]}
    />
)};
const mapStateToProps = (state) => ({
  destinations: state.connections.destinations || [],
});
export default connect(mapStateToProps)(Destinations);
