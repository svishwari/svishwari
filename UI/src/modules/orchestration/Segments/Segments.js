import React from 'react';
import { useDispatch } from "react-redux";
import CTPrimaryButton from '../../../components/Button/CTPrimaryButton';
import { showAddSegment } from '../../modal/action';

const Segments = () => {
    const dispatch = useDispatch();
    return (
        <CTPrimaryButton 
        onKeyPress={()=> dispatch(showAddSegment({initialScreen: 1,initialSelected: ["Churn", "Propensity", "Life Time Value"]}))} 
        onClick={()=> dispatch(showAddSegment({initialScreen: 1,initialSelected: ["Churn", "Propensity", "Life Time Value"]}))} 
        >
            Add Segment
        </CTPrimaryButton>
    )
}
export default Segments
