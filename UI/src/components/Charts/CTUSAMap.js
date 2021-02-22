import React, { useRef, useEffect } from "react";
import "./CTUSAMap.scss";
import USAMap from "react-usa-map";

interface IProps {
  data?: [];
}

const CTUSAMap = (props: IProps) => {
  const convertHexToRGBA = (hexCode, opacity) => {
    let hex = hexCode.replace("#", "");

    if (hex.length === 3) {
      hex = `${hex[0]}${hex[0]}${hex[1]}${hex[1]}${hex[2]}${hex[2]}`;
    }

    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);

    return `rgba(${r},${g},${b},${opacity / 100})`;
  };
  const mapData = () => {
    if (props.data) {
      props.data.map((state) => {});
      return props.data.reduce((result, item, index) => {
        const key = Object.keys(item)[0]; // first property: a, b, c
        const valueObj = {};
        valueObj.fill = convertHexToRGBA("#0076A8", item[key]);
        result[key] = valueObj;
        return result;
      }, {});
    }
  };
  const chartContainer = useRef(null);
  return (
    <div className="usChart">
      <USAMap
        ref={chartContainer}
        customize={mapData()}
        defaultFill="#FFFFFF"
      />
    </div>
  );
};

export default CTUSAMap;
