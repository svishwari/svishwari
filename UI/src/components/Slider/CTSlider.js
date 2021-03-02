import React, { useState } from "react";
import "./CTSlider.scss";
import { Range, getTrackBackground } from "react-range";

const CTSlider = ({
  minValue = 0.0,
  maxValue = 1.0,
  stepSize = 0.05,
  customClass = "",
  ...sliderprops
}) => {
  const STEP = stepSize;
  const MIN = minValue;
  const MAX = maxValue;

  const [values, setValues] = useState([0.1, 0.55]);

  return (
    <div className={`ct-slider-wrapper ${customClass}`}>
      <Range
        values={values}
        step={STEP}
        min={MIN}
        max={MAX}
        onChange={(newValues) => {
          setValues(newValues);
        }}
        {...sliderprops}
        renderTrack={({ props, children }) => (
          <div
            onMouseDown={props.onMouseDown}
            onTouchStart={props.onTouchStart}
            style={{
              ...props.style,
              background: getTrackBackground({
                values,
                colors: ["#F7F8FA", "#43B02A", "#F7F8FA"],
                min: MIN,
                max: MAX,
              }),
            }}
          >
            <div ref={props.ref} className="ct-slider-track">
              {children}
            </div>
          </div>
        )}
        renderThumb={({ props }) => (
          <div
            {...props}
            style={{
              ...props.style,
            }}
            className="ct-slider-thumb"
          >
            {props["aria-valuenow"] === values[0] ? (
              <>{values[0].toFixed(2)}</>
            ) : (
              <>{values[1].toFixed(2)}</>
            )}
          </div>
        )}
      />
    </div>
  );
};

export default CTSlider;
