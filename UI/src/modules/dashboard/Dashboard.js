import React from "react";
import { connect, useDispatch } from "react-redux";
import DonutChart from "react-d3-donut/es";
import CTUSAMap from "../../components/Charts/CTUSAMap";
import CTPrimaryButton from "../../components/Button/CTPrimaryButton";

import { showAddDataSource } from "../modal/action";

const Dashboard = () => {
  const dispatch = useDispatch();
  const usData = [{ TX: 90 }, { NY: 28 }, { WA: 68 }, { CA: 18 }];
  const SegmentData = [
    { name: "MostLikely", count: 70, color: "#00A99D" },
    { name: "High Likely", count: 30, color: "#E89F74" },
    { name: "Likely", count: 250, color: "#DA5B41" },
    { name: "UnLikely", count: 150, color: "#9AA4AF" },
  ];
  return (
    <div>
      {/* <button onClick={() => retrieveMetrics() } >Click Me</button> */}
      <h2>WorldMap</h2>
      <div className="d-flex">
        <CTUSAMap data={usData} />
        <DonutChart
          innerRadius={70}
          outerRadius={100}
          transition
          displayTooltip
          strokeWidth={3}
          svgClass="segmentDonut"
          pieClass="pie6"
          data={SegmentData}
        />
      </div>
      <CTPrimaryButton onClickFn={()=> dispatch(showAddDataSource())}>Click me!</CTPrimaryButton>
    </div>
  );
};
const mapStateToProps = (state) => ({
  posts: state.dashboardReducer.user || [],
  modal: state.modal,
});
export default connect(mapStateToProps)(Dashboard);
