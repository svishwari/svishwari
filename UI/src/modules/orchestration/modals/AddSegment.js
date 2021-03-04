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
import CTSelect from "../../../components/Select/CTSelect";
import CTSlider from "../../../components/Slider/CTSlider";
// import CTSwitch from "../../../components/Switch/CTSwitch";

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
const OPERAND_OPTIONS = ["AND", "OR"]

const AddSegment = (props) => {
    const dispatch = useDispatch();
    const { initialScreen, initialSelected=[] } = props;
    const [selectedModels, setSelectedModels] = useState(initialSelected);

    const BASE_VALUES = {
        model: selectedModels[0],
        min: 0.20,
        max: 0.70,
    };

    const CONDITION_TEMPLATE = {
        conditions: [BASE_VALUES],
        operand: "AND"
    };

    const SEGMENT_TEMPLATE = {
        segmentName: "",
        segmentConditions: [CONDITION_TEMPLATE],
    };

    const [segments, setSegments] = useState([SEGMENT_TEMPLATE]);

    const addNewSegment = () => {
        const newArrayOfSegments = [...segments,SEGMENT_TEMPLATE];
        setSegments(newArrayOfSegments);
    }

    const onSegmentNameChange = (e,segmentIndex) => {
        const newSegmentName = e.target.value;
        const segmentWithNewName = segments[segmentIndex];
        segmentWithNewName.segmentName = newSegmentName;

        setSegments([...segments.slice(0, segmentIndex),
                        segmentWithNewName,
                    ...segments.slice(segmentIndex+1)
                    ]);
    }

    const addRule = (segmentIndex,condIndex) => {
        const oldConditions = segments[segmentIndex].segmentConditions[condIndex].conditions;
        const newConditions = [...oldConditions,BASE_VALUES];
        const newLevel = [
            ...segments[segmentIndex].segmentConditions.slice(0, condIndex),
            {conditions: newConditions,operand: segments[segmentIndex].segmentConditions[condIndex].operand},
            ...segments[segmentIndex].segmentConditions.slice(condIndex+1)
        ]
        const newSegment = [...segments.slice(0, segmentIndex),
            {segmentConditions: newLevel,segmentName: segments[segmentIndex].segmentName},
        ...segments.slice(segmentIndex+1)
        ]
        setSegments(newSegment);
    }

    const addSubRule = (segmentIndex) => {
        const newSubRule = [...segments[segmentIndex].segmentConditions,CONDITION_TEMPLATE];
        setSegments([...segments.slice(0, segmentIndex),
            {segmentConditions: newSubRule,segmentName: segments[segmentIndex].segmentName},
        ...segments.slice(segmentIndex+1)
        ]);
    }
    const toggleSelectedModels = (model) => {
        const modelIndex = selectedModels.indexOf(model);
        if ( modelIndex !== -1) {
            const newArray = selectedModels.filter(each=> each!==model);
            setSelectedModels(newArray);
        }
        else {
            setSelectedModels([...selectedModels,model] );
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
                    customClass={selectedModels.indexOf(model.title) !== -1 ? "model-selected" : "" }
                    cardImage={<span className="ct-add-segment-image">{model.image}</span>}
                    cardTitle={model.title} 
                    onClick={()=> {toggleSelectedModels(model.title)}  }
                    cardDescription={model.desc}
                />
               ))
            }
        </CTCardGroup>

    </div>);
    const screen2 = (
    <div className="ct-segment-screen2-wrapper">
        <div>Condition/Rule Name</div>
            { segments.map((segment,segmentIndex)=>(
                    <div>
                        <div className="ct-condition-wrapper">
                            <div className="ct-condition-container">
                                <CTInput onChangeFunc={(e)=>onSegmentNameChange(e,segmentIndex)} placeholder="Segment Name"/>
                            </div>
                        </div>
                        {
                            segment.segmentConditions.map( (cond,condIndex) => (
                                <>
                                    <div style={{paddingLeft: condIndex*20, }} className="ct-add-rule-wrapper">
                                        <CTSecondaryButton onClickFn={()=>addSubRule(segmentIndex)} customClass="mr-2">+ Add Sub-Condition</CTSecondaryButton>
                                        <CTSecondaryButton onClickFn={()=>addRule(segmentIndex,condIndex)}>+ Add Condition</CTSecondaryButton>
                                        <CTSelect customClass="ct-operand-select-wrapper" selectOptions={OPERAND_OPTIONS} />
                                    </div>
                                    {
                                        cond.conditions.map( (condition) => (
                                            <div style={{paddingLeft: condIndex*20}}>
                                                <div className="ct-rule-arrow-extended" />
                                                <div className="ct-rule-wrapper">
                                                    <div className="ct-rule-arrow" />
                                                    <CTSelect customClass="ct-rule-select" selectOptions={selectedModels} />
                                                    <CTSlider initialMinValue={condition.min} initialMaxValue={condition.max} customClass="ct-rule-slider"/>
                                                </div>
                                            </div>
                                        ))
                                    }
                                </>
                            ))
                        }
                    </div>
            )) 
            }
        <div>
            <span className="add-condition-icon" onClick={addNewSegment} onKeyPress={addNewSegment}>
                <span className="iconify" data-icon="mdi:plus-circle" data-inline="false" />
            </span>
            Segment
        </div>
    </div>);
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
        rightButtonProps: [{isDisabled: selectedModels.length===0 },{},{}],
        screenTitle: ["Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                        "You are required to have at least one condition!",
                        "This is optional - you can always deliver later."
                    ]
    }

    return (
        <CTModal
            modalTitle="Add Segments"
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
