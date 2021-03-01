import React from 'react';
import { useDispatch } from "react-redux";
import CTPrimaryButton from '../../../components/Button/CTPrimaryButton';
import { showAddSegment } from '../../modal/action';

const Segments = () => {
    const dispatch = useDispatch();
    return (
        <CTPrimaryButton 
        onKeyPress={()=> dispatch(showAddSegment())} 
        onClick={()=> dispatch(showAddSegment())} 
        >
            Add Segment
        </CTPrimaryButton>
    )
}
export default Segments
