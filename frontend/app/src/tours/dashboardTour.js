import { driver } from 'driver.js'
import 'driver.js/dist/driver.css'
import '@/assets/main.css'

const desktopSteps = (showSleepForm) => [
  {
    popover: {
      title: 'Welcome to King Of Sleep',
      description: `
        <p class="mb-5">
          King Of The Sleep turns your real sleep data into the performance of your avatar in a competitive auto-battle game.
        </p>
  
        <p class="mb-5">
          Every day, up to 100 players compete in the same arena. The day runs from 10:00 to 23:00 and is divided into several automatic battle rounds.
        </p>

        <p class="mb-5">
          Your sleep duration, efficiency, consistency, REM sleep and deep sleep determine how your avatar performs. After every round, the player and protocol rankings are updated.
        </p>

        <p class="mb-5">
          Let’s take a quick look at how the dashboard works.
        </p>
      `,
    },
  },
  {
    element: '#next-battle',
    popover: {
      title: 'Next battle',
      description:
        'King Of The Sleep is divided into rounds. Here you can see the <b>countdown</b> to the next battle and how your <b>ranking position</b> changed after the previous round.',
    },
  },
  {
    element: '#battle',
    popover: {
      title: 'The arena',
      description:
        'This is the arena, where you can watch your automatic battles against other players. Your sleep data determines how your character performs.',
    },
  },
  {
    element: '#today-stats',
    popover: {
      title: "Today's stats",
      description:
        'Track your performance throughout the day, including battles played, victories, defeats and your win rate.',
    },
  },
  {
    element: '#ranking',
    popover: {
      title: 'Player ranking',
      description:
        'After every round, the ranking is updated according to the battle results. Keep improving your sleep to climb higher.',
    },
  },
  {
    element: '#protocols',
    popover: {
      title: 'Protocol ranking',
      description:
        'Protocols move up or down depending on the battle results of the players using them. See which protocols are performing best and worst.',
    },
  },
  {
    element: '#user-profile',
    popover: {
      title: 'Your profile',
      description:
        'View your player progression, global ranking and the sleep score generated from your most recent night.',
    },
  },
  {
    element: '#sleep-score',
    popover: {
      title: 'Sleep score',
      description:
        'Follow the evolution of your overall sleep quality over the last seven days and see whether your sleep is improving.',
    },
  },
{
  element: '#protocol-impact',

  popover: {
    title: 'Protocol impact',
    description:
      'Discover which protocols were associated with your best and worst sleep. Use these results to decide which habits to keep, change or remove.',

    onNextClick: async (_element, _step, { driver }) => {
      await showSleepForm()
        driver.moveNext()
    },
  },
},
  {
    element: '#sleep-form',
    popover: {
      title: 'Daily sleep check-in',
      description:
        'Every morning, the arena closes at 11:00. Submit the previous night’s sleep data before that time to participate in that day’s battles.',
    },
  },
]

const mobileSteps = (showSleepForm) => [
    {
    popover: {
      title: 'Welcome to King Of Sleep',
      description: `
        <p>
          King Of The Sleep turns your real sleep data into the performance of your avatar in a competitive auto-battle game.
        </p>

        <p>
          Every day, up to 100 players compete in the same arena. The day runs from 10:00 to 23:00 and is divided into several automatic battle rounds.
        </p>

        <p>
          Your sleep duration, efficiency, consistency, REM sleep and deep sleep determine how your avatar performs. After every round, the player and protocol rankings are updated.
        </p>

        <p>
          Sleep better, win more battles and climb the rankings.
        </p>
      `,
    },
  },
  {
    element: '#next-battle-mobile',
    popover: {
      title: 'Next battle',
      description:
        'King Of The Sleep is divided into rounds. Here you can see the countdown to the next battle and how your ranking position changed after the previous round.',
    },
  },
  {
    element: '#battle-mobile',
    popover: {
      title: 'The arena',
      description:
        'This is the arena, where you can watch your automatic battles against other players. Your sleep data determines how your character performs.',
    },
  },
  {
    element: '#today-stats-mobile',
    popover: {
      title: "Today's stats",
      description:
        'Track your performance throughout the day, including battles played, victories, defeats and your win rate.',
    },
  },
  {
    element: '#ranking-mobile',
    popover: {
      title: 'Player ranking',
      description:
        'After every round, the ranking is updated according to the battle results. Keep improving your sleep to climb higher.',
    },
  },
  {
    element: '#protocols-mobile',
    popover: {
      title: 'Protocol ranking',
      description:
        'Protocols move up or down depending on the battle results of the players using them. See which protocols are performing best and worst.',
    },
  },
  {
    element: '#profile-mobile',
    popover: {
      title: 'Your profile',
      description:
        'View your player progression, global ranking and the sleep score generated from your most recent night.',
    },
  },
  {
    element: '#sleep-score-mobile',
    popover: {
      title: 'Sleep score',
      description:
        'Follow the evolution of your overall sleep quality over the last seven days and see whether your sleep is improving.',
    },
  },
{
  element: '#protocol-impact-mobile',

  popover: {
    title: 'Protocol impact',
    description:
      'Discover which protocols were associated with your best and worst sleep. Use these results to decide which habits to keep, change or remove.',

    onNextClick: async (_element, _step, { driver }) => {
      await showSleepForm()
        driver.moveNext()
    },
  },
},
  {
    element: '#sleep-form-mobile',
    popover: {
      title: 'Daily sleep check-in',
      description:
        'Every morning, the arena closes at 11:00. Submit the previous night’s sleep data before that time to participate in that day’s battles.',
    },
  },
]

export function startDashboardTour(showSleepForm, onCompleted) {
  const isMobile = window.innerWidth < 1024

  const driverObj = driver({
    popoverClass: 'kots-driver-popover',
    animate: true,
    disableActiveInteraction: true,
    smoothScroll: true,
    showProgress: true,
    allowClose: false,

    steps: isMobile
      ? mobileSteps(showSleepForm)
      : desktopSteps(showSleepForm),

    onDoneClick: () => {
      onCompleted?.()
      driverObj.destroy()
    },
  })

  driverObj.drive()
}