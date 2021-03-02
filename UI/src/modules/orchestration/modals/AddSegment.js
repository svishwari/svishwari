import React, { useState, useEffect } from 'react';
import { connect, useDispatch } from "react-redux";
import { Link } from "react-router-dom";

import CTModal from "../../../components/Modal/CTModal";
import CTLabel from "../../../components/Label/CTLabel";
import CTInput from "../../../components/Input/CTInput";
import CTCardGroup from "../../../components/Cards/CardGroup/CTCardGroup";
import CTImageCard from "../../../components/Cards/ImageCard/CTImageCard";
import CTSecondaryButton from "../../../components/Button/CTSecondaryButton";
import CTDataGrid from "../../../components/Table/CTDataGrid";

import { hideModal } from "../../modal/action";
import {
    fetchDestinations,
} from "../../connections/store/action";

import "./AddSegment.scss";
import { ReactComponent as  ChurnIcon } from "../../../assets/icons/churn-icon.svg";
import { ReactComponent as  Propensity } from "../../../assets/icons/propensity.svg";
import { ReactComponent as  LifeTimeValue } from "../../../assets/icons/life-time-value.svg";

const AVAILABLE_MODELS = [
    {
        title: "Churn",
        image: <ChurnIcon />,
        desc: "Identify customers and their characteristics that are likely to leave your service or product."
    },
    {
        title: "Propensity",
        image: <Propensity />,
        desc: "The likelihood of a lead to convert and/or purchse based on desired characteristics."
    },
    {
        title: "Life Time Value",
        image: <LifeTimeValue />,
        desc: "Predicts lifetime value of your customers based on time, cost of acquisition, cost of sale, etc."
    },
];

const AddSegment = (props) => {
    const { initialScreen } = props;
    const [selectedModels, setSelectedModels] = useState(new Set());
    const dispatch = useDispatch();
    const toggleSelectedModels = (model) => {
        const newSet = new Set(selectedModels);
        if (selectedModels.has(model)) {
            newSet.delete(model);
            setSelectedModels(newSet);
        } else {
            newSet.add(model);
            setSelectedModels(newSet);
        }
    }
    const onCloseAndCompleteLater = () => {
        // Dispatch some api call here
        dispatch(hideModal());
    }
    const fetchScore = () => {
        // Dispatch some api call here
    }
    const retrieveDestinations = () => {
        // Dispatch some api call here
        dispatch(fetchDestinations());
    }
    const columns = [
        {
            field: "destination",
            headerName: " ",
            width: 50,
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
                </>
            )},
        },
        {
            field: "destinationName",
            headerName: "Destination",
            width: 600,
            renderCell: (params) => (
                <>
                <Link to="/destinations">
                    {`${params.getValue("destinationName")} `}
                    <span
                    className="iconify"
                    data-icon="mdi:open-in-new"
                    data-inline="false"
                    />
                </Link>
                </>
            ),
        },
        {
          field: "account",
          headerName: "Account Name",
          width: 200,
        }, 
    ];

    useEffect(() => {
        retrieveDestinations();
    }, [])



    const screen1 = (<div className="ct-segment-screen1-wrapper">
        <CTCardGroup>
            <span className="ct-add-segment-card">
                <CTLabel>Segment Name</CTLabel>
                <CTInput placeholder="My Amazing Segment"/>
            </span>
            <span className="ct-add-segment-card">
                <CTLabel>File Source</CTLabel>
                <CTInput placeholder="Select" />
            </span>

        </CTCardGroup>
        <div className="ct-add-segment-label">Select Model(s) <span className="ct-add-segment-label-light">(You can select more than one)</span></div>
        <CTCardGroup>
            {
               AVAILABLE_MODELS.map(model => (
                <CTImageCard 
                    key={model.title}
                    customClass={selectedModels.has(model.title) ? "model-selected" : "" }
                    cardImage={<span className="ct-add-segment-image">{model.image}</span>}
                    cardTitle={model.title} 
                    onClick={()=> {toggleSelectedModels(model.title)}  }
                    cardDescription={model.desc}
                />
               ))
            }
        </CTCardGroup>

    </div>);
    const screen2 = (<div>Screen 2</div>);
    const screen3 = (
    <div className="ct-segment-screen3-wrapper">
        <div className="ct-segment-screen3-title">Select Destination(s)</div>
        <div className="ct-segment-screen3-table">
            <CTDataGrid 
                isTopVisible={false}
                isEditingEnabled
                columns={columns}
                data={props.destinations}
                // TO DO ON SELECTED ROWS DO SOMETHING HERE 
                onRowSelect={()=> {}}
            />
        </div>
    </div>);

    const screens = {
        screenComponents: [screen1,screen2,screen3],
        righButtonFunctions: [fetchScore,()=>{},()=>{}],
        righButtonNames: ["Fetch Scores & Continue","Continue","Deliver & Complete"],
        rightButtonProps: [{isDisabled: selectedModels.size===0 },{},{}],
        screenTitle: ["Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                        "You are required to have at least one condition!",
                        "This is optional - you can always deliver later."
                    ]
    }

    return (
        <CTModal
            modalTitle="Add a Segment"
            startScreenNumber={initialScreen}
            screens={screens}
            footerLeftButtons={[
                (<CTSecondaryButton customClass="segment-btn-later" key="1" activeindex={1}  onClick={onCloseAndCompleteLater}>
                    Close &amp; Complete Later 
                </CTSecondaryButton>),
                (<CTSecondaryButton customClass="segment-btn-later" key="2" activeindex={2}  onClick={onCloseAndCompleteLater}>
                Close &amp; Complete Later 
            </CTSecondaryButton>)]}
            maxWidth="lg"
        />
    )
}

const mapStateToProps = (state) => ({
    destinations: state.connections.destinations || [],
  });
export default connect(mapStateToProps)(AddSegment);
