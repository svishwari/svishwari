import React from 'react';
import CTModal from "../../../components/Modal/CTModal";
import CTLabel from "../../../components/Label/CTLabel";
import CTInput from "../../../components/Input/CTInput";
import CTCardGroup from "../../../components/Cards/CardGroup/CTCardGroup";
import CTImageCard from "../../../components/Cards/ImageCard/CTImageCard";
import "./AddSegment.scss";
import { ReactComponent as  ChurnIcon } from "../../../assets/icons/churn-icon.svg";
import { ReactComponent as  Propensity } from "../../../assets/icons/propensity.svg";
import { ReactComponent as  LifeTimeValue } from "../../../assets/icons/life-time-value.svg";

const AddSegment = (props) => {
    const { initialScreen } = props;
    const screen1 = (<div className="ct-segment-screen1-wrapper">
        <CTCardGroup>
            <span className="ct-add-segment-card">
                <CTLabel>Segment Name</CTLabel>
                <CTInput />
            </span>
            <span className="ct-add-segment-card">
                <CTLabel>File Source</CTLabel>
                <CTInput />
            </span>

        </CTCardGroup>
        <CTCardGroup>
            <CTImageCard 
                cardImage={<span className="ct-add-segment-image"><ChurnIcon /></span>}
                cardTitle="Churn" 
                cardDescription="Identify customers and their characteristics that are likely to leave your service or product."
            />
            <CTImageCard 
                cardImage={<span className="ct-add-segment-image"><Propensity /></span>}
                cardTitle="Propensity" 
                cardDescription="The likelihood of a lead to convert and/or purchse based on desired characteristics."
            />
            <CTImageCard 
                cardImage={<span className="ct-add-segment-image"><LifeTimeValue /></span>}
                cardTitle="Life Time Value"
                cardDescription="Predicts lifetime value of your customers based on time, cost of acquisition, cost of sale, etc."
            />
        </CTCardGroup>

    </div>);
    const screen2 = (<div>Screen 2</div>);
    const screen3 = (<div>Screen 3</div>);

    const screens = {
        screenComponents: [screen1,screen2,screen3],
        righButtonFunctions: [()=>{},()=>{},()=>{}],
        righButtonNames: ["Fetch Scores & Continue","Continue","Deliver & Complete"],
        rightButtonProps: [{},{},{}],
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
            maxWidth="lg"
        />
    )
}

export default AddSegment
