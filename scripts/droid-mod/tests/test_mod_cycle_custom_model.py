import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path("/Users/zhenninglang/.dotfiles/scripts/droid-mod/mods/mod_cycle_custom_model.py")
STATUS = Path("/Users/zhenninglang/.dotfiles/scripts/droid-mod/status.py")
DIRECT_CALLBACK_MARKER = (
    b'GR().getCustomModels().map((gA)=>gA.id);'
    b"if(RR.length<=1)return;"
)
FILTERED_DIRECT_CALLBACK_MARKER = (
    b'GR().getCustomModels().map((gA)=>gA.id).filter((gA)=>!gA.includes("["));'
    b"if(RR.length<=1)return;"
)
COMPACT_FILTERED_CALLBACK_TAIL = (
    b'let oR=VT();if(gA=RR[(RR.indexOf(oR.hasSpecModeModel()?oR.getSpecModeModel():oR.getModel())+1)%RR.length])Yk(gA)'
)
SUPER_COMPACT_CALLBACK_MARKER = (
    b'let RR=jG.filter(g=>!g.includes("[")),o=VT();'
)
SUPER_COMPACT_CALLBACK_TAIL = (
    b'RR[1]&&HV(RR[RR.indexOf(o.hasSpecModeModel()&&o.getSpecModeModel()||o.getModel())+1]||RR[0])'
)
BROKEN_SUPER_COMPACT_CALLBACK_MARKER = (
    b'let RR=Y8A().filter(g=>!g.includes("[")),o=VT();'
)
BROKEN_SUPER_COMPACT_CALLBACK_TAIL = (
    b'RR[1]&&Yk(RR[RR.indexOf(o.hasSpecModeModel()&&o.getSpecModeModel()||o.getModel())+1]||RR[0])'
)
CURRENT_SUPER_COMPACT_CALLBACK_MARKER = (
    b'let RR=lw.filter(g=>!g.includes("[")),o=VT();'
)
ORIGINAL_CALLBACK_BYTES = (
    b"fu=M9.useCallback(()=>{if(jG.length<=1)return;let PA=QZ().getModelPolicy();if(!jG.some((g)=>AB(g,PA).allowed))return;SW((x)=>!x)},[jG]),"
    b"HV=M9.useCallback(async(RR)=>{return RR},[AA])"
)

BROKEN_PATCHED_BYTES = (
    b"peekNextCycleModel(H,T){H=this.customModels.map(m=>m.id);if(H.length===0)return null;let R=T??this.getModel(),A=H.indexOf(R),B=A===-1?0:A;"
    b"for(let D=1;D<=H.length;D++){let C=(B+D)%H.length,I=H[C];/*            */try{let O=PJ(I);return{modelId:I,effort:O}}catch{continue}}return null}"
    b"cycleModel(H,T){let R=this.peekNextCycleModel(H,T);if(!R)return T??this.getModel();return this.setModel(R.modelId,R.effort),R.modelId}"
    b"peekNextCycleSpecModeModel(H,T){H=this.customModels.map(m=>m.id);if(H.length===0)return null;let R=T??this.getSpecModeModel(),A=H.indexOf(R),B=A===-1?0:A;"
    b"for(let D=1;D<=H.length;D++){let C=(B+D)%H.length,I=H[C];/*            */try{let O=PJ(I);return{modelId:I,effort:O}}catch{continue}}return null}"
    b"cycleSpecModeModel(H){H=this.customModels.map(m=>m.id);if(H.length===0)return this.getSpecModeModel();let T=this.getSpecModeModel(),R=H.indexOf(T),A=R===-1?0:R;"
    b"for(let B=1;B<=H.length;B++){let D=(A+B)%H.length,C=H[D];/*            */try{let $=PJ(C);return this.setSpecModeModel(C,$),C}catch{continue}}return T}"
    b"ul=K9.useCallback(()=>{let BR=GR().peekNextCycleModel(Y8A(),VT().hasSpecModeModel()?VT().getSpecModeModel():VT().getModel());if(BR)Yk(BR.modelId)},[lw]),"
    b"Yk=K9.useCallback(async(RR)=>{DL(!1);let oR=VT();if(oR.isSpecMode()&&oR.hasSpecModeModel()){let JB=oR.getSpecModeModel();if(RR===JB)return;"
    b"let xL=OB(RR).defaultReasoningEffort,JL=await g2(RR,xL);if(!JL.success)return;if(wI({specModeModelId:RR,specModeReasoningEffort:xL,interactionMode:oR.getInteractionMode()}),JL.compactionPerformed)O9()}"
    b"else{let JB=oR.getModel();if(RR===JB)return;let xL=OB(RR).defaultReasoningEffort,JL=await hU(RR,xL);if(!JL.success)return;if(wI({modelId:RR,reasoningEffort:xL}),JL.compactionPerformed)O9()}},[hU,g2,wI])"
)

CURRENT_BROKEN_CALLBACK_BYTES = (
    b"ul=K9.useCallback(()=>{let RR=GR().peekNextCycleModel(lw,VT().hasSpecModeModel()?VT().getSpecModeModel():null);if(RR)Yk(RR.modelId)},[lw]),"
    b"Yk=K9.useCallback(async(RR)=>{DL(!1);let oR=VT();if(oR.isSpecMode()&&oR.hasSpecModeModel()){let JB=oR.getSpecModeModel();if(RR===JB)return;"
    b"let xL=OB(RR).defaultReasoningEffort,JL=await g2(RR,xL);if(!JL.success)return;if(wI({specModeModelId:RR,specModeReasoningEffort:xL,interactionMode:oR.getInteractionMode()}),JL.compactionPerformed)O9()}"
    b"else{let JB=oR.getModel();if(RR===JB)return;let xL=OB(RR).defaultReasoningEffort,JL=await hU(RR,xL);if(!JL.success)return;if(wI({modelId:RR,reasoningEffort:xL}),JL.compactionPerformed)O9()}},[hU,g2,wI])"
)


def _write_droid(home: Path, data: bytes) -> Path:
    droid = home / ".local/bin/droid"
    droid.parent.mkdir(parents=True, exist_ok=True)
    droid.write_bytes(data)
    return droid


def _run(script: Path, home: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["HOME"] = str(home)
    return subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


class ModCycleCustomModelTests(unittest.TestCase):
    def test_patches_original_callback_with_shorter_filtered_cycle_logic(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir)
            droid = _write_droid(home, ORIGINAL_CALLBACK_BYTES)

            result = _run(SCRIPT, home)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            patched = droid.read_bytes()
            self.assertIn(SUPER_COMPACT_CALLBACK_MARKER, patched)
            self.assertIn(SUPER_COMPACT_CALLBACK_TAIL, patched)
            self.assertLessEqual(len(patched) - len(ORIGINAL_CALLBACK_BYTES), 32)

            status = _run(STATUS, home)
            self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
            self.assertIn("mod-cycle-custom-model: 已修改", status.stdout)

    def test_repairs_broken_patch_and_status_detects_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir)
            droid = _write_droid(home, BROKEN_PATCHED_BYTES)

            result = _run(SCRIPT, home)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            patched = droid.read_bytes()
            self.assertNotEqual(patched, BROKEN_PATCHED_BYTES)
            self.assertEqual(patched.count(b"this.customModels.map(m=>m.id)"), 0)
            self.assertEqual(patched.count(b"validateModelAccess("), 3)
            self.assertIn(BROKEN_SUPER_COMPACT_CALLBACK_MARKER, patched)
            self.assertIn(BROKEN_SUPER_COMPACT_CALLBACK_TAIL, patched)
            self.assertNotIn(
                b"peekNextCycleModel(lw,VT().hasSpecModeModel()?VT().getSpecModeModel():null)",
                patched,
            )
            self.assertNotIn(b"if(BR)Yk(BR.modelId)", patched)

            rerun = _run(SCRIPT, home)
            self.assertEqual(rerun.returncode, 0, rerun.stdout + rerun.stderr)
            self.assertIn("已应用", rerun.stdout)

            status = _run(STATUS, home)
            self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
            self.assertIn("mod-cycle-custom-model: 已修改", status.stdout)

    def test_repairs_current_lw_based_callback(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir)
            droid = _write_droid(home, CURRENT_BROKEN_CALLBACK_BYTES)

            result = _run(SCRIPT, home)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            patched = droid.read_bytes()
            self.assertIn(CURRENT_SUPER_COMPACT_CALLBACK_MARKER, patched)
            self.assertIn(BROKEN_SUPER_COMPACT_CALLBACK_TAIL, patched)
            self.assertNotIn(
                b"peekNextCycleModel(lw,VT().hasSpecModeModel()?VT().getSpecModeModel():null)",
                patched,
            )


if __name__ == "__main__":
    unittest.main()
