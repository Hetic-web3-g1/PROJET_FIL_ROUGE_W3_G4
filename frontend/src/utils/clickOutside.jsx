import React, { useRef, useEffect } from "react";
import PropTypes from "prop-types";


export const OutsideAlerter = ({ returnValues, ...props }) => {
  const wrapperRef = useRef(null);
  useOutsideAlerter(wrapperRef);

  return <div ref={wrapperRef}>{props.children}</div>;

  /**
   * Hook that alerts clicks outside of the passed ref
   * @param {HTMLElement} ref HTML element clicked by the user
   */
  function useOutsideAlerter(ref) {
    useEffect(() => {

      /**
       * On click detect if the HTML element selected contains the HTML element we want to hide
       * @param {HTMLElement} elementToHide HTML element we want to hide
       */
      function handleClickOutside(elementToHide) {
        if (ref.current && !ref.current.contains(elementToHide.target)) {
          returnValues(true);
        }
      }
      // Bind the event listener
      document.addEventListener("mousedown", handleClickOutside);
      return () => {
        // Unbind the event listener on clean up
        document.removeEventListener("mousedown", handleClickOutside);
      };
    }, [ref]);
  }
}


OutsideAlerter.propTypes = {
  children: PropTypes.element.isRequired,
  returnValues: PropTypes.func.isRequired, // function needed in parent to hide the HTML element
};

export default OutsideAlerter;