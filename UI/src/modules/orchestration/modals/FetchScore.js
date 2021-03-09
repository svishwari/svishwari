import React from 'react';
import { useDispatch } from "react-redux";
import CTModal from "../../../components/Modal/CTModal";
import { ReactComponent as HUX_LOGO } from "../../../assets/hux_logo.svg";
import CTSecondaryButton from '../../../components/Button/CTSecondaryButton';
import { hideModal } from '../../modal/action';

const FetchScore = () => {
    const dispatch = useDispatch();
    const staticScreen = (
        <div>
            <HUX_LOGO />
            <h3 className="p-4">Fetching Scores...</h3>
            <h6 className="pb-4">This may take up to 30 seconds, so feel free to stand up and stretch your legs or close and come back later. </h6>
            <CTSecondaryButton btnWidth={215} onClickFn={()=>dispatch(hideModal())}>Save &amp; Continue Later</CTSecondaryButton>
        </div>
    )
    return (
        <CTModal
            maxWidth="md"
            modalBody={staticScreen}
            showFooter={false}
        />
    )
}

export default FetchScore;
