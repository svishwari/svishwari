import React from 'react';
import { connect, useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import { Box, Button } from '@material-ui/core';

import { showAddSegment } from '../../modal/action';
import { fetchSegments, triggerDeliveredCheck } from "../store/action";

import CTDataGrid from "../../../components/Table/CTDataGrid";
import CTChip from "../../../components/Chip/CTChip";
import CTPopover from "../../../components/Popover/CTPopover";

const FILTER_TYPES = {
    "Starred": {
      selectMultiple: false,
      values: ["Starred", "Not Starred"]
    },
    "Deliver Status": {
      selectMultiple: true,
      values: ["Delivered", "Not Delivered"]
    },
};

const markDelivering = (payload) => ({
    type: "updateDeliverStatus",
    payload,
});

const Segments = (props) => {
    const dispatch = useDispatch();
    const retrieveSegments = () => {
        dispatch(fetchSegments());
    };
    const markDelivered = (id) => {
        dispatch(triggerDeliveredCheck(id));
    };
    React.useEffect(() => {
        retrieveSegments();
    }, []);
    const columns = [
        {
          field: "segmentName",
          headerName: "Segment Name",
          flex: 0.2,
          // TO DO Check how to apply this class only when the isDraft is true
          cellClassName: "overflow-visible",
          renderCell: (params) => {
            const openAddSegment = () => {
              dispatch(showAddSegment({initialScreen: 1,initialSelected: params.row.models,isDraft: true,id: params.getValue("id") }));
            }
            if( params.getValue("isDraft")){
              return (
              <div>Segment Name (Draft)
                <Link onKeyPress={openAddSegment} onClick={openAddSegment} to={()=>false}>
                  &nbsp;Continue Configuring &gt;
                </Link>
              </div>)
            }
            return (
            <Link to={`/orchestration/segments/${params.getValue("id")}`}>
              {params.getValue("segmentName")}
            </Link>
          )},
        },
        {
            field: "deliverStatus",
            headerName: "Status",
            flex: 0.15,
            renderCell: (params) => {
              const triggerDelivery = () => {
                const payload = {
                  id: params.getValue("id"),
                  status: "Delivering...",
                };
                dispatch(markDelivering(payload));
                markDelivered(params.getValue("id"));
              };
              if( params.getValue("isDraft")){
                return (<></>);
              }
              return (
                <>
                  {params.getValue("deliverStatus") !== "Delivering..." ? (
                    <CTChip
                      hasIcons
                      isWorking={params.getValue("deliverStatus") === "Delivered"}
                      onClickFunc={triggerDelivery}
                    >
                      {params.getValue("deliverStatus")}
                    </CTChip>
                  ) : (
                    <span>Delivering...</span>
                  )}
                </>
              );
            },
        },
        {
          field: "models",
          headerName: "Model(s)",
          flex: 0.1,
          renderCell: (params) => {
            const modelsLength = params.getValue("models").length;
            if( params.getValue("isDraft")){
              return (<></>);
            }
            if( modelsLength === 1) {
              return (
                <div>{params.getValue("models")[0]}</div>
              )
            }
            return (
              <CTPopover
                popoverContent={
                    params.getValue("models").map((each,index)=> (
                      <span>{each}{index!== modelsLength-1 && ", "}</span>
                    ))
                }
                trigger="hover"
              >
                <div>
                  <span style={{borderBottom: "1px dashed #767676", cursor: "pointer"}}>{modelsLength} Selected</span>
                </div>
              </CTPopover>
            )
          },
        },
        {
          field: "size",
          headerName: "Size",
          flex: 0.15,
          renderCell: (params) => {
            if( params.getValue("isDraft")){
              return (<></>);
            }
            return <div>{params.getValue("size")}</div>
          }
        },
        {
          field: "created",
          headerName: "Created",
          flex: 0.15,
        },
        {
            field: 'open',
            headerName: ' ',
            flex: 0.2,
            renderCell: () => (
              <CTPopover
                popoverContent={
                  <Box display="flex" flexDirection="column">
                    <Button><span className="iconify" data-icon="logos:facebook" data-inline="false" />{'\u00A0'}Facebook</Button>
                    <Button><span className="iconify" data-icon="logos:google-analytics" data-inline="false" />{'\u00A0'}Google</Button>
                  </Box>
                }
              >
                <Button color="primary" style={{ textTransform: 'capitalize' }}>
                  Open in <span className="iconify" data-icon="zmdi-caret-down" data-inline="false" />
                </Button>
              </CTPopover>
            ),
          },
    ];
    return (
        <CTDataGrid
            data={props.segments}
            columns={columns}
            hasStarring
            loading={!props.segments.length}
            pageName="Segment"
            isTopVisible
            onAddClick={()=> dispatch(showAddSegment())}
            filterTypes={FILTER_TYPES}
            moreIconContent={[{name: "Configure", function: ()=> {} },]}
            enableMoreIcon
        />
    )
}
const mapStateToProps = (state) => ({
    segments: state.orchestration.segments || [],
  });
export default connect(mapStateToProps)(Segments);
