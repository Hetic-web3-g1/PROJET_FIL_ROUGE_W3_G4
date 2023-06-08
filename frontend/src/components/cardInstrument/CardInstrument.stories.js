import { CardInstrument } from './CardInstrument';

export default {
  title: 'Card Instrument',
  component: CardInstrument
};

export const Base = {
  args: {
  },
};

export const CustomSVG = {
  args: {
    name: 'Trombone',
  },
};

export const CustomSize = {
  args: {
    name: 'Trombone',
    size: 50
  },
};

export const HasLegend = {
  args: {
    name: 'Trombone',
    legend: true
  },
};