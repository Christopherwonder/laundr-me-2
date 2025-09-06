import React from "react";
import { render, fireEvent } from "@testing-library/react-native";
import KYCScreen from "../KYCScreen";

describe("KYCScreen", () => {
  it("renders correctly", () => {
    const { getByText, getByPlaceholderText } = render(<KYCScreen />);

    expect(getByText("Let's get you verified")).toBeTruthy();
    expect(getByPlaceholderText("Enter your full name")).toBeTruthy();
    expect(getByText("Submit & Continue")).toBeTruthy();
  });

  it("calls onKycVerified when submit button is pressed with a valid name", () => {
    const onKycVerified = jest.fn();
    const { getByText, getByPlaceholderText } = render(
      <KYCScreen onKycVerified={onKycVerified} />,
    );

    const input = getByPlaceholderText("Enter your full name");
    fireEvent.changeText(input, "John Doe");

    const submitButton = getByText("Submit & Continue");
    fireEvent.press(submitButton);

    expect(onKycVerified).toHaveBeenCalledWith(true);
  });

  it("does not call onKycVerified when submit button is pressed with an empty name", () => {
    const onKycVerified = jest.fn();
    const { getByText } = render(<KYCScreen onKycVerified={onKycVerified} />);

    const submitButton = getByText("Submit & Continue");
    fireEvent.press(submitButton);

    expect(onKycVerified).not.toHaveBeenCalled();
  });
});
