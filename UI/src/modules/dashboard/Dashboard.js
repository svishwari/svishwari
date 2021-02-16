import React from 'react';
import { connect } from "react-redux";
import CTPrimaryButton from '../../components/Button/CTPrimaryButton';
import CTSecondaryButton from '../../components/Button/CTSecondaryButton';
import CTTertiaryButton from '../../components/Button/CTTertiaryButton';

// import CTToast from '../../components/Toast/CTToast';
import CTSlider from '../../components/Slider/CTSlider';
import CTInput from '../../components/Input/CTInput';
import CTLabel from '../../components/Label/CTLabel';
import CTCardGroup from '../../components/Cards/CardGroup/CTCardGroup';
import CTImageCard from '../../components/Cards/ImageCard/CTImageCard';
import { ReactComponent as VideoIcon } from "../../assets/icons/video-shooting.svg";
import CTSimpleCard from '../../components/Cards/SimpleCard/CTSimpleCard';
import CTWorldMap from '../../components/Charts/CTWorldMap';
const Dashboard = (props) => {

    return (
        <div>
            <h1>StyleGuide</h1>
            {/* <button onClick={() => retrieveMetrics() } >Click Me</button> */}
            <h2>WorldMap</h2>
            <CTWorldMap />
            <div className="btnExamples">
                <h2>Buttons</h2>
                <div className='mb-2'>
                <CTPrimaryButton>Primary</CTPrimaryButton>
                <CTPrimaryButton isDisabled={true}>Primary</CTPrimaryButton>
                </div>
                <div className='mb-2'>
                <CTSecondaryButton>Secondary</CTSecondaryButton>
                <CTSecondaryButton isDisabled={true}>Secondary</CTSecondaryButton>
                </div>
                <div className='mb-2'>
                <CTTertiaryButton>Tertiary Button</CTTertiaryButton>
                <CTTertiaryButton isDisabled={true}>Tertiary Button</CTTertiaryButton>
                </div>
            </div>
            <div>
                <h2>Cards</h2>
                <CTCardGroup>
                    <CTImageCard cardImage={(<VideoIcon />)} cardDescription='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.Lorem ipsum dolor sit amet, consectetur adipiscing elit.'></CTImageCard>
                    <CTImageCard cardImage={( <span className="iconify" data-icon="mdi:emoticon-happy" data-inline="false"></span> )} cardDescription='Lorem ipsum dolor sit amet, consectetur adipiscing elit.'></CTImageCard>
                    <CTImageCard imageColor='#00C395' cardImage={( <span className="iconify" data-icon="mdi:emoticon-happy" data-inline="false"></span> )} cardDescription='Lorem ipsum dolor sit amet, consectetur adipiscing elit.'></CTImageCard>
                    <CTImageCard cardImage={( <span className="iconify" data-icon="mdi:emoticon-happy" data-inline="false"></span> )} cardDescription='Lorem ipsum dolor sit amet, consectetur adipiscing elit.'></CTImageCard>
                    <CTImageCard cardImage={( <span className="iconify" data-icon="mdi:emoticon-happy" data-inline="false"></span> )} cardDescription='Lorem ipsum dolor sit amet, consectetur adipiscing elit.'></CTImageCard>
                    <CTSimpleCard>
                        Hello world
                    </CTSimpleCard>
                </CTCardGroup>
            </div>
            <div>
                <h2>Input</h2>
                <CTLabel>Email</CTLabel>
                <CTInput inputType='text'/>
                <CTLabel>Password</CTLabel>
                <CTInput inputType='password'/>
                <CTLabel>Some input</CTLabel>
                <CTInput errorMessage='Oh no! There is some error' inputType='text'/>
            </div>
            <h2>Slider</h2>
            <div>
            <CTSlider />
            </div>
        </div>
    )
}
const mapStateToProps = state => {
    return {
        posts: state.dashboardReducer.user || []
    };
};
export default connect(mapStateToProps)(Dashboard);