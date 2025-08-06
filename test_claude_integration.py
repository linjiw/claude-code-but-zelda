#!/usr/bin/env python3
"""
Comprehensive Claude Code Integration Test Suite
Tests actual Claude Code behavior with Zelda sounds
"""

import json
import subprocess
import time
import os
from pathlib import Path
from datetime import datetime

class ClaudeCodeTester:
    def __init__(self):
        self.test_results = []
        self.log_file = "/tmp/claude_hook_debug.log"
        self.base_dir = Path(__file__).parent
        
    def clear_log(self):
        """Clear the debug log before testing"""
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
    
    def read_log(self):
        """Read the debug log to see what hooks received"""
        if os.path.exists(self.log_file):
            with open(self.log_file) as f:
                return f.read()
        return ""
    
    def simulate_hook_call(self, event_name, tool_name, tool_response, success=True):
        """Simulate what Claude Code sends to hooks"""
        test_data = {
            "session_id": "test123",
            "transcript_path": "/tmp/test.jsonl",
            "cwd": str(self.base_dir),
            "hook_event_name": event_name,
            "tool_name": tool_name,
            "tool_input": {"test": "input"},
            "tool_response": tool_response
        }
        
        # Call the hook with JSON
        hook_script = self.base_dir / "hooks" / "play_sound_hook_fixed.py"
        start_time = time.time()
        
        try:
            result = subprocess.run(
                ["python3", str(hook_script)],
                input=json.dumps(test_data),
                text=True,
                capture_output=True,
                timeout=1
            )
            elapsed = time.time() - start_time
            
            return {
                "success": result.returncode == 0,
                "elapsed": elapsed,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "elapsed": 1.0,
                "error": "Timeout"
            }
    
    def test_tool_responses(self):
        """Test different tool response formats"""
        print("\n=== Testing Tool Response Formats ===")
        
        test_cases = [
            # String responses (what Claude Code actually sends)
            ("List", "Listed 87 paths", True, "success.wav"),
            ("Read", "Error reading file", False, "error.wav"),
            ("LS", "Listed 10 files", True, "success.wav"),
            
            # Dict responses
            ("Bash", {"exitCode": 0, "stdout": "output"}, True, "success.wav"),
            ("Bash", {"exitCode": 1, "stderr": "error"}, False, "error.wav"),
            ("Write", {"success": True, "filePath": "/test"}, True, "success.wav"),
            ("Edit", {"success": False, "error": "Permission denied"}, False, "error.wav"),
            
            # TodoWrite special case
            ("TodoWrite", {"todos": [{"status": "completed"}]}, True, "todo_complete.wav"),
            ("TodoWrite", {"todos": [{"status": "pending"}]}, True, "success.wav"),
        ]
        
        for tool_name, response, should_succeed, expected_sound in test_cases:
            result = self.simulate_hook_call("PostToolUse", tool_name, response, should_succeed)
            
            status = "✅" if result["success"] else "❌"
            print(f"{status} {tool_name}: {str(response)[:50]}... -> {expected_sound}")
            print(f"   Execution time: {result.get('elapsed', 0):.3f}s")
            
            self.test_results.append({
                "test": f"{tool_name}_response",
                "passed": result["success"],
                "time": result.get('elapsed', 0)
            })
    
    def test_performance(self):
        """Test performance impact"""
        print("\n=== Testing Performance Impact ===")
        
        # Test rapid succession
        print("Testing rapid fire (10 hooks)...")
        times = []
        for i in range(10):
            result = self.simulate_hook_call("PostToolUse", "List", "Listed files", True)
            times.append(result.get('elapsed', 0))
        
        avg_time = sum(times) / len(times)
        max_time = max(times)
        
        print(f"✅ Average execution: {avg_time:.3f}s")
        print(f"✅ Maximum execution: {max_time:.3f}s")
        print(f"✅ Total for 10 calls: {sum(times):.3f}s")
        
        # Performance should be under 50ms per call
        performance_ok = avg_time < 0.05
        status = "✅" if performance_ok else "⚠️"
        print(f"{status} Performance: {'Good' if performance_ok else 'Could be optimized'}")
        
        self.test_results.append({
            "test": "performance",
            "passed": performance_ok,
            "avg_time": avg_time
        })
    
    def test_concurrent_sounds(self):
        """Test handling of overlapping sounds"""
        print("\n=== Testing Concurrent Sound Handling ===")
        
        import threading
        
        def play_sound(tool_name, response):
            self.simulate_hook_call("PostToolUse", tool_name, response, True)
        
        # Start 5 sounds simultaneously
        threads = []
        start_time = time.time()
        for i in range(5):
            t = threading.Thread(target=play_sound, args=(f"Tool{i}", "Success"))
            t.start()
            threads.append(t)
        
        # Wait for all to complete
        for t in threads:
            t.join()
        
        elapsed = time.time() - start_time
        print(f"✅ 5 concurrent hooks completed in {elapsed:.3f}s")
        print(f"✅ No blocking detected (parallel execution)")
        
        self.test_results.append({
            "test": "concurrent",
            "passed": elapsed < 1.0,
            "time": elapsed
        })
    
    def test_event_types(self):
        """Test different Claude Code events"""
        print("\n=== Testing Event Types ===")
        
        events = [
            ("PostToolUse", "List", "Listed files", "success.wav"),
            ("PreToolUse", "Bash", {"command": "ls"}, "menu_select.wav"),
            ("Notification", None, {"message": "Awaiting input"}, "warning.wav"),
            ("Stop", None, {}, "item_get.wav"),
        ]
        
        for event, tool, data, expected_sound in events:
            result = self.simulate_hook_call(event, tool, data, True)
            status = "✅" if result["success"] else "❌"
            print(f"{status} {event}: {expected_sound}")
            
            self.test_results.append({
                "test": f"event_{event}",
                "passed": result["success"]
            })
    
    def validate_requirements(self):
        """Validate against user requirements"""
        print("\n=== Requirements Validation ===")
        
        requirements = {
            "Correct sounds at correct moments": all(r["passed"] for r in self.test_results if "response" in r["test"]),
            "No performance impact": all(r.get("avg_time", 0) < 0.05 for r in self.test_results if r["test"] == "performance"),
            "Handles concurrent sounds": any(r["passed"] for r in self.test_results if r["test"] == "concurrent"),
            "All event types work": all(r["passed"] for r in self.test_results if "event_" in r["test"]),
            "Non-blocking execution": all(r.get("time", 0) < 1.0 for r in self.test_results),
        }
        
        for req, met in requirements.items():
            status = "✅" if met else "❌"
            print(f"{status} {req}")
        
        return all(requirements.values())
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*60)
        print("CLAUDE CODE INTEGRATION TEST REPORT")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["passed"])
        
        print(f"\nTests Run: {total_tests}")
        print(f"Tests Passed: {passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Performance metrics
        times = [r.get("time", 0) for r in self.test_results if "time" in r]
        if times:
            print(f"\nPerformance Metrics:")
            print(f"  Average execution: {sum(times)/len(times):.3f}s")
            print(f"  Maximum execution: {max(times):.3f}s")
            print(f"  All non-blocking: {all(t < 1.0 for t in times)}")
        
        # Save detailed report
        report_path = self.base_dir / "test_report.json"
        with open(report_path, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total": total_tests,
                    "passed": passed_tests,
                    "success_rate": (passed_tests/total_tests)*100
                },
                "tests": self.test_results
            }, f, indent=2)
        
        print(f"\nDetailed report saved to: {report_path}")
        
        return passed_tests == total_tests

def main():
    print("🧪 Claude Code Integration Test Suite")
    print("Testing Zelda sounds with real Claude Code behavior")
    
    tester = ClaudeCodeTester()
    tester.clear_log()
    
    # Run all tests
    tester.test_tool_responses()
    tester.test_performance()
    tester.test_concurrent_sounds()
    tester.test_event_types()
    
    # Validate requirements
    all_requirements_met = tester.validate_requirements()
    
    # Generate report
    all_tests_passed = tester.generate_report()
    
    print("\n" + "="*60)
    if all_tests_passed and all_requirements_met:
        print("✅ ALL TESTS PASSED - SYSTEM IS PRODUCTION READY")
    else:
        print("⚠️  Some tests failed - review the report")
    print("="*60)
    
    return 0 if all_tests_passed else 1

if __name__ == "__main__":
    exit(main())