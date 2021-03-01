import React from 'react';
import CTModal from "../../../components/Modal/CTModal";

const AddSegment = (props) => {
    const { initialScreen } = props;
    const screen1 = (<div>Screen 1</div>);
    const screen2 = (<div>Screen 2</div>);
    const screen3 = (<div>Screen 3</div>);

    const screens = {
        screenComponents: [screen1,screen2,screen3],
        righButtonFunctions: [()=>{},()=>{},()=>{}],
        righButtonNames: ["Fetch Scores & Continue","Continue","Deliver & Complete"],
        rightButtonProps: [{},{isDisabled: true},{}],
    }

    return (
        <CTModal
            modalTitle="Add a Segment"
            modalSubtitle="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
            modalBody={initialScreen}
            mainCTAText="Verify and Add"
            startScreenNumber={initialScreen}
            screens={screens}
        />
    )
}

export default AddSegment
