import Dropdown from "./Dropdown";

export default {
  title: 'Dropdown',
  component: Dropdown
};

export const Base = {
  args: {
  },
};

export const CustomOptions = {
  args: {
  options: ['This', 'Is', 'A', 'Custom', 'Dropdown'],
  },
};

export const DisabledOption = {
  args: {
  options: ['This', 'Is', 'A', 'Custom', 'Dropdown'],
  disabled: true
  },
};