import tempfile, unittest
from pathlib import Path
from lottery_sync_demo import GUARDS, LotteryScheduler, Process, example_processes, render_gantt

class LotteryTests(unittest.TestCase):
    def test_same_trace_for_all_modes(self):
        traces=[]
        for mode in GUARDS:
            s=LotteryScheduler(example_processes(),mode,seed=19)
            traces.append([(x.pid,x.start,x.end,x.winning_ticket) for x in s.run()])
        self.assertEqual(traces[0],traces[1]); self.assertEqual(traces[1],traces[2])
    def test_seed_reproducibility(self):
        self.assertEqual(LotteryScheduler(example_processes(),seed=5).run(),
                         LotteryScheduler(example_processes(),seed=5).run())
    def test_all_processes_finish(self):
        s=LotteryScheduler(example_processes()); trace=s.run()
        self.assertTrue(trace); self.assertTrue(all(p.remaining==0 for p in s.processes.values()))
    def test_ticket_bounds(self):
        s=LotteryScheduler(example_processes()); s.run()
        self.assertTrue(all(1<=t<=total for _,_,t,total in s.draws))
    def test_metrics(self):
        s=LotteryScheduler(example_processes()); s.run()
        for m in s.metrics().values():
            self.assertEqual(m["waiting"]+m["burst"],m["turnaround"])
            self.assertGreaterEqual(m["waiting"],0)
    def test_arrival_time(self):
        s=LotteryScheduler([Process("late",2,1,arrival=4)]); trace=s.run()
        self.assertEqual((trace[0].start,trace[-1].end),(4,6))
    def test_empty_workload(self):
        s=LotteryScheduler([],mode="monitor"); self.assertEqual(s.run(),[]); self.assertEqual(s.metrics(),{})
    def test_bad_inputs(self):
        with self.assertRaises(ValueError): LotteryScheduler([],mode="bad")
        with self.assertRaises(ValueError): LotteryScheduler([],quantum=0)
        with self.assertRaises(ValueError): Process("P",0,1)
        with self.assertRaises(ValueError): Process("P",1,0)
        with self.assertRaises(ValueError): LotteryScheduler([Process("P",1,1),Process("P",2,2)])
    def test_gantt_svg(self):
        s=LotteryScheduler(example_processes()); 
        with tempfile.TemporaryDirectory() as d:
            p=render_gantt(s.run(),Path(d)/"gantt.svg")
            self.assertIn("<svg",p.read_text()); self.assertIn("P1",p.read_text())
if __name__=="__main__": unittest.main(verbosity=2)
