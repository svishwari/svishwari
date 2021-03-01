import React from 'react';
import { useDispatch } from "react-redux";
import CTPrimaryButton from '../../../components/Button/CTPrimaryButton';
import { showAddSegment } from '../../modal/action';

const Segments = () => {
    const dispatch = useDispatch();
    return (
        <CTPrimaryButton 
        onKeyPress={()=> dispatch(showAddSegment({initialScreen: 1}))} 
        onClick={()=> dispatch(showAddSegment({initialScreen: 1}))} 
        >
            Add Segment
        </CTPrimaryButton>
    )
}
export default Segments
