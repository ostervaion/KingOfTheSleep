import { driver } from 'driver.js'
import 'driver.js/dist/driver.css'

const desktopSteps = [
  {
    element: '#next-battle',
    popover: {
      title: 'Next battle',
      description: 'See when the next battle begins.',
    },
  },
  {
    element: '#battle',
    popover: {
      title: 'Battle',
      description: 'Watch your current battle.',
    },
  },
  {
    element: '#today-stats',
    popover: {
      title: "Today's stats",
      description: 'See your performance today.',
    },
  },
  {
    element: '#ranking',
    popover: {
      title: 'Ranking',
      description: 'See your current ranking.',
    },
  },
  {
    element: '#protocols',
    popover: {
      title: 'Protocols',
      description: 'See the most effective protocols.',
    },
  },
  {
    element: '#user-profile',
    popover: {
      title: 'Profile',
      description: 'See your player profile.',
    },
  },
  {
    element: '#sleep-score',
    popover: {
      title: 'Sleep score',
      description: 'See your recent sleep score.',
    },
  },
  {
    element: '#protocol-impact',
    popover: {
      title: 'Protocol impact',
      description: 'See how protocols affect performance.',
    },
  },
]

const mobileSteps = [
  {
    element: '#next-battle-mobile',
    popover: {
      title: 'Next battle',
      description: 'See when the next battle begins.',
    },
  },
  {
    element: '#battle-mobile',
    popover: {
      title: 'Battle',
      description: 'Watch your current battle.',
    },
  },
  {
    element: '#today-stats-mobile',
    popover: {
      title: "Today's stats",
      description: 'See your performance today.',
    },
  },
  {
    element: '#ranking-mobile',
    popover: {
      title: 'Ranking',
      description: 'See your current ranking.',
    },
  },
  {
    element: '#protocols-mobile',
    popover: {
      title: 'Protocols',
      description: 'See the most effective protocols.',
    },
  },
  {
    element: '#profile-mobile',
    popover: {
      title: 'Profile',
      description: 'See your player profile.',
    },
  },
  {
    element: '#sleep-score-mobile',
    popover: {
      title: 'Sleep score',
      description: 'See your recent sleep score.',
    },
  },
  {
    element: '#protocol-impact-mobile',
    popover: {
      title: 'Protocol impact',
      description: 'See how protocols affect performance.',
    },
  },
]

export function startDashboardTour() {
  const isDesktop = window.matchMedia('(min-width: 1024px)').matches

  const driverObj = driver({
    showProgress: true,
    allowClose: false,
    popoverClass: 'kots-driver-popover',
    steps: isDesktop ? desktopSteps : mobileSteps,
  })

  driverObj.drive()

  return driverObj
}