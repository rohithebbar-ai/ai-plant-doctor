#!/usr/bin/env python3
"""
Comprehensive test runner for AI Plant Doctor

This script runs all tests with detailed reporting and coverage analysis.
"""

import unittest
import sys
import os
import time
from io import StringIO

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def run_all_tests():
    """Run all test suites with comprehensive reporting"""
    
    print("🌱 AI Plant Doctor - Test Suite Runner")
    print("=" * 50)
    
    # Discover and load all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Count total tests
    total_tests = suite.countTestCases()
    print(f"📊 Discovered {total_tests} tests")
    print("-" * 50)
    
    # Create detailed test runner
    stream = StringIO()
    runner = unittest.TextTestRunner(
        stream=stream,
        verbosity=2,
        buffer=True,
        failfast=False
    )
    
    # Run tests with timing
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Get output
    test_output = stream.getvalue()
    
    # Print results
    print("📋 Test Results:")
    print("-" * 50)
    
    # Print test output (but filter for important parts)
    lines = test_output.split('\n')
    for line in lines:
        if any(keyword in line for keyword in ['test_', 'ERROR', 'FAIL', 'OK', '...']):
            if 'test_' in line and ('OK' in line or 'FAIL' in line or 'ERROR' in line):
                status = "✅" if "OK" in line else "❌" if "FAIL" in line else "💥"
                test_name = line.split()[0]
                print(f"{status} {test_name}")
    
    print("-" * 50)
    
    # Summary statistics
    duration = end_time - start_time
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    
    print(f"📊 Summary:")
    print(f"   Total Tests:    {result.testsRun}")
    print(f"   ✅ Passed:      {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   ❌ Failed:      {len(result.failures)}")
    print(f"   💥 Errors:      {len(result.errors)}")
    print(f"   📈 Success Rate: {success_rate:.1f}%")
    print(f"   ⏱️  Duration:    {duration:.2f} seconds")
    
    # Print failures and errors if any
    if result.failures:
        print("\n❌ FAILURES:")
        print("-" * 30)
        for test, traceback in result.failures:
            print(f"Test: {test}")
            print(f"Error: {traceback[:200]}...")
            print()
    
    if result.errors:
        print("\n💥 ERRORS:")
        print("-" * 30)
        for test, traceback in result.errors:
            print(f"Test: {test}")
            print(f"Error: {traceback[:200]}...")
            print()
    
    # Final status
    if result.wasSuccessful():
        print("\n🎉 All tests passed! Your code is working correctly.")
    else:
        print(f"\n⚠️  {len(result.failures) + len(result.errors)} test(s) failed. Please check the errors above.")
    
    print("=" * 50)
    
    return result.wasSuccessful()


def run_specific_test_file(test_file):
    """Run tests from a specific file"""
    print(f"🧪 Running tests from {test_file}")
    print("-" * 30)
    
    # Import the specific test module
    module_name = test_file.replace('.py', '')
    try:
        test_module = __import__(module_name)
        
        # Load tests from module
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(test_module)
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
        
    except ImportError as e:
        print(f"❌ Could not import {module_name}: {e}")
        return False


def check_test_dependencies():
    """Check if all required modules can be imported"""
    print("🔍 Checking test dependencies...")
    
    required_modules = [
        'unittest',
        'PIL',
        'torch',
        'sys',
        'os'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - Not found")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️  Missing modules: {', '.join(missing_modules)}")
        print("Please install missing dependencies with:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies available")
    return True


def main():
    """Main test runner entry point"""
    
    if len(sys.argv) > 1:
        # Run specific test file
        test_file = sys.argv[1]
        if test_file.endswith('.py'):
            success = run_specific_test_file(test_file)
        else:
            print(f"❌ Invalid test file: {test_file}")
            success = False
    else:
        # Check dependencies first
        if not check_test_dependencies():
            sys.exit(1)
        
        # Run all tests
        success = run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()